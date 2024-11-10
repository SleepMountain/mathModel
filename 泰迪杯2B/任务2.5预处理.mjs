import fs from 'fs';


const data = JSON.parse(fs.readFileSync('../output-WithRightUnit.json', 'utf8'));

let odata = []
for (let tyid in data) {
    let item = data[tyid];
    odata.push( item["【适用人群】"])
    // result[tyid] = {
    //     "脂肪": nuti["脂肪"]["每100g"],
    //     "蛋白质": nuti["蛋白质"]["每100g"],
    // }
}
fs.writeFileSync('../output-Task2.5.txt', odata.join("\n"), 'utf8')