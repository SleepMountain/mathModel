import { match } from 'assert';
import fs from 'fs';
import path from 'path';
import { exit } from 'process';

const input_dir = "./output";
let csv_rawdata = {}
let csv_data = [];
fs.readdir(input_dir, (err, files) => {
    // files = [files[1]]
    files.forEach(file => {
        if (path.extname(file) === ".txt") {
            const TYID = file.match(/TY(\d+)/)[1];
            csv_rawdata[TYID] = {};
            const input_file = path.join(input_dir, file);
            const output_file = path.join(input_dir, file.replace(".txt", ".csv"));
            const data = fs.readFileSync(input_file, "utf8")

            //1. 查询所有【?<HEADERNAME>(.*)】位置并以此为分割
            const headers = [...data.matchAll(/【(.*?)】/g)].map(match => "【" + match[1] + "】");
            headers.unshift("");


            const body = headers.map((header, index) => {
                //2.1 获取当前分割的内容
                const start = data.indexOf(header) + header.length
                const end = (index === headers.length - 1 ? data.length : data.indexOf(headers[index + 1]))
                const content = data.substring(start, end).trim();
                return content;
            })
            headers[0] = "【基本信息】";
            body[0] = body[0].replace(/(\r|\n)/g, "<BLANK>");

            const info = body[0].split("<BLANK>").filter(row => row)
            //console.log(info)
            //info中从前往后找到第一个以食品结尾的行，将其之后的行合并为名字
            const name_index = info.findIndex(row => row.match(/食品$|配方粉$|补充剂$|配方奶$/));

            const name = info.slice(name_index + 1).join("-").replace(/(\r|\n| )/g, "").replace(/®/g, "");
            headers.unshift("【公司】");
            body.unshift(name);
            headers.unshift("【名称】");
            body.unshift(info[name_index]);



            headers.forEach((header, index) => {
                headers[index] = header.replace(/(\r|\n| )/g, "")
            })

            headers.map((header, index) => {
                csv_rawdata[TYID][header] = body[index];
            })
            //3. 单独拆离营养成分表
            delete csv_rawdata[TYID]["【营养成分表】"];

            //读取nutrition表格
            const nutrition_file = JSON.parse(fs.readFileSync(path.join(input_dir, file.replace(".txt", ".json")), "utf8"));
            //合并json
            let nutrition_data = []
            nutrition_file.forEach(row => {
                nutrition_data = nutrition_data.concat(row);
            })
            nutrition_data = nutrition_data.filter(row => row && row.length > 1 && row[0]);
            let nutrition_header = nutrition_data.shift();

            nutrition_data = nutrition_data.filter(row => row && row[0] && row.length === nutrition_header.length && !row[0].match(/营养成分|婴儿|对照|比|国际|月|周/));

            for (let i = 0; i < nutrition_data.length; i++) {
                //如果一个数据只有0有值，1无值，则视为是上一行错误换行下来的，将0合并到上一行的0
                if (nutrition_data[i][1] === "") {
                    if (nutrition_data[i - 1][0].match(/\)$/) && i !== nutrition_data.length - 1) {
                        nutrition_data[i + 1][0] = nutrition_data[i][0] + nutrition_data[i + 1][0]
                        nutrition_data[i] = [];
                    } else {
                        nutrition_data[i - 1][0] += nutrition_data[i][0];
                        nutrition_data[i] = [];
                    }
                }
            }
            nutrition_data = nutrition_data.filter(row => row && row[0]);
            for(let i = 0; i < nutrition_data.length; i++){
                for(let j = 0; j < nutrition_data[i].length; j++){
                    if(nutrition_data[i][j].match(/\n/) && nutrition_data[i][j][nutrition_data[i][j].indexOf("\n") + 1].match(/\d/)){
                        //将\n后的数字挪到括号左侧
                        const index = nutrition_data[i][j].indexOf("\n");
                        const number = nutrition_data[i][j].substring(index + 1);
                        const the_left_bracket = (nutrition_data[i][j].indexOf("(")+1 || nutrition_data[i][j].indexOf("（")+1)-1
                        nutrition_data[i][j] = nutrition_data[i][j].substring(0, the_left_bracket) + number + nutrition_data[i][j].substring(the_left_bracket,index);
                    }
                    nutrition_data[i][j] = nutrition_data[i][j]
                    .replace(/(\r|\n| )/g, "")
                    .replace(/（/g, "(")
                    .replace(/）/g, ")")
                }
            }

            
            csv_rawdata[TYID]["【营养成分表】"] = {}
            for(let n of nutrition_data){
                csv_rawdata[TYID]["【营养成分表】"][n[0]] = {}
                for(let i = 1; i < n.length; i++){
                    csv_rawdata[TYID]["【营养成分表】"][n[0]][nutrition_header[i]] = n[i];
                    //匹配到中文字符，报错
                    // if(n[i].match(/[\u4e00-\u9fa5]/)){
                    //     console.error(`[] TYID:${TYID} ${n[0]} ${nutrition_header[i]} ${n[i]}`);
                    // }
                }
            }


            // 考虑到表格格式和错行问题，最后还是单独用pdfplumber额外提取表格实现，至少能避免单元格内数据紊乱，以下为原先处理代码
            // const note = nutrition.match(/备注：(.*)/) ? nutrition.match(/备注：(.*)/)[0] : "";
            // csv_rawdata[TYID]["【营养成分表备注】"] = note
            // nutrition = nutrition.replace(/备注：(.*)/, "").replace(/无/, "");

            // let nutrition_data = nutrition.split("\n")
            // //寻找以营养成分为开头的那一列，将其定义为header
            // let headerindex = nutrition_data.findIndex(row => row.match(/营养成分/));
            // let header = nutrition_data[headerindex].split(/ /)
            // header = header.filter(h => h && h.trim()).map(h => h.trim()).slice(1);

            // //处理nutrition异常数据
            // //1.移除所有带有营养成分的行
            // nutrition_data = nutrition_data.filter(row => !row.match(/营养成分/));
            // //2.将每行开始不为两个空格的行合并到上一行
            // for (let i = 0; i < nutrition_data.length; i++) {
            //     if (nutrition_data[i].match(/  /)) {
            //         nutrition_data[i - 1] += nutrition_data[i];
            //         nutrition_data[i] = "";
            //     }
            // }
            // nutrition_data = nutrition_data.filter(row => row);
            // //3.将长度大于8后所有数字后面跟的不是纯文本的部分踢到下一行
            // for (let i = 0; i < nutrition_data.length; i++) {
            //     let row = nutrition_data[i].split(/ /);
            //     if (row.length > 8) {
            //         let last = row.pop();
            //         if (!last.match(/[a-zA-Z]/)) {
            //             nutrition_data[i] = row.join(" ");
            //             nutrition_data[i + 1] = last + nutrition_data[i + 1];
            //         }
            //     }
            // }


            // csv_rawdata[TYID]["【营养成分表】"] = {};
            // for (let row of nutrition_data) {

            //     if (!row || row.match(/营养成分|比值/)) {
            //         continue;
            //     }
            //     row = row.replace(/（/g, "(").replace(/）/g, ")").replace(/，/g, ",").replace(/：/g, ":");
            //     if (row.match(/\(|\)/)) {
            //         const the_final_next_right_bracket = row.lastIndexOf(")");
            //         //以此为分割线，将前面部分割离为key，后面部分割离为value
            //         let key = row.substring(0, the_final_next_right_bracket + 1);
            //         //查询key钟最左侧的括号位置，并将其之前作为主键
            //         const left_bracket = key.indexOf("(");
            //         let main_key = key.substring(0, left_bracket).replace(/ /g, "");
            //         if (!main_key) {
            //             continue;
            //         }
            //         //将key中的括号内容作为单位键
            //         let unit = key.substring(left_bracket + 1, key.length - 1);
            //         csv_rawdata[TYID]["【营养成分表】"][main_key] = {};
            //         csv_rawdata[TYID]["【营养成分表】"][main_key].unit = `(${unit.trim()})`
            //         csv_rawdata[TYID]["【营养成分表】"][main_key].data = {};
            //         let value = row.substring(the_final_next_right_bracket + 1).trim().split(/ /);
            //         for (let i = 0; i < header.length; i++) {
            //             csv_rawdata[TYID]["【营养成分表】"][main_key].data[header[i]] = value[i];
            //         }
            //     } else {
            //         row = row.trim().split(/ /);
            //         let main_key = row[0];
            //         if(!main_key){
            //             continue;
            //         }
            //         if (main_key.match(/\d/)) {
            //             console.log(main_key);
            //             console.log(`[] TYID:${TYID} ${main_key}`);
            //         }
            //         csv_rawdata[TYID]["【营养成分表】"][main_key] = {};
            //         csv_rawdata[TYID]["【营养成分表】"][main_key].data = {};
            //         for (let i = 1; i < header.length; i++) {
            //             csv_rawdata[TYID]["【营养成分表】"][main_key].data[header[i]] = row[i];
            //             //如果存在非数字的数据，console.error
            //             if (!row[i]) {
            //                 console.log(`[] TYID:${TYID} ${main_key} ${header[i]} ${row[i]}`);
            //             }
            //             //如果header中存在含有数字的数据，console.error
            //             if (header[i].match(/\d/)) {
            //                 console.log(`[] TYID:${TYID} ${main_key} ${header[i]} ${row[i]}`);
            //             }
            //         }
            //         csv_rawdata[TYID]["【营养成分表】"][main_key].unit = "";
            //     }




            // }
            for (let key in csv_rawdata[TYID]) {
                if (typeof csv_rawdata[TYID][key] === "string") {
                    csv_rawdata[TYID][key] = csv_rawdata[TYID][key].replace(/(\r|\n| )/g, "");
                }
            }
        }
        
    });
    fs.writeFileSync("output.json", JSON.stringify(csv_rawdata, null, 4), "utf8");
    //fs.writeFileSync("output.csv", csv_data.map(row => row.join("|")).join("\n"), "utf8");
})
