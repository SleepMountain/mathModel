//用于修正单位 并额外添加 企业名称  产品名称 注册证号 有效期至  适用人群类别 产品来源 登记年份
import fs from 'fs';


//读取json
const data = JSON.parse(fs.readFileSync('output.json', 'utf8'));

//读取csv
const csv = fs.readFileSync('data.csv', 'utf8').replace(/\r/g, "").split('\n').map(e => e.split(','))
const csvHeader = csv.shift();
const csvObj = {}
csv.forEach(e => {
    console.log(e)
    csvObj[e[2].replace("国食注字TY", "")] = e;
})


const unit = ["g", "mg", "μg","kJ"]
const unitMap = [1000000, 1000, 1,1]


for (let tyid in data) {
    let item = data[tyid];
    item['【企业名称】'] = csvObj[tyid][0].replace(/，/g, ",")
    item['【产品名称】'] = csvObj[tyid][1];
    item['【注册证号】'] = csvObj[tyid][2];
    item['【有效期至】'] = csvObj[tyid][3];
    item['【适用人群类别】'] = item["【适用人群】"].match(/婴儿/g) ? "特医婴配食品" : "1岁以上特医食品"
    item['【产品来源】'] = tyid.slice(4, 5) == "5" ? "进口产品" : "国产产品";
    item['【登记年份】'] = tyid.slice(0, 4);
    //营养物质匹配
    let final_nuts = {}
    let item_nuts = item["【营养成分表】"];
    for (let nut_name in item_nuts) {
        nut_name = nut_name.replace(/，/g, ",")
        if (nut_name.match(/\%|比/g)) {
            console.log(`${tyid} ${nut_name} 应当被移除`)
            continue;
        }
        let nut_realunit = ((name, units) => {
            for (let unit of units) {
                if (name.match(`\\(${unit}`)) {
                    return unit;
                }
            }
            return null;
        })(nut_name, unit)
        if (!nut_realunit) {
            console.log(`!!${tyid} ${nut_name} 未找到单位`)
            continue;
        }
        const nut_name_without_units = nut_name.slice(0, nut_name.indexOf("("))
        final_nuts[nut_name_without_units] = {}

        console.log(`- ${tyid} ${nut_name} 单位是 ${nut_realunit}`)
        Object.keys(item_nuts[nut_name]).forEach(i => {
            console.log(`${i} ${item_nuts[nut_name][i]} 倍率 ${unitMap[unit.indexOf(nut_realunit)]}`)
            final_nuts[nut_name_without_units][i] = Number(item_nuts[nut_name][i]) * unitMap[unit.indexOf(nut_realunit)]
            console.log(`修正为 ${item_nuts[nut_name][i]}`)
        })
        item["【营养成分表】"] = final_nuts;
    }
}

fs.writeFileSync('output-WithRightUnit.json', JSON.stringify(data, null, 4), 'utf8');