import fs from 'fs';


const data = JSON.parse(fs.readFileSync('../output-WithRightUnit.json', 'utf8'));
const odata = {

}

let result = [
    ["注册证号", "每100kJ脂肪含量", "每100ml脂肪含量", "每100g脂肪含量", "每100kJ蛋白质含量", "每100ml蛋白质含量", "每100g蛋白质含量"]
]
for (let tyid in data) {
    let item = data[tyid];
    let nuti = item["【营养成分表】"]
    result.push([
        tyid,
        nuti["脂肪"]["每100kJ"] || 0,
        nuti["脂肪"]["每100mL"] || 0,
        nuti["脂肪"]["每100g"] || 0,
        nuti["蛋白质"]["每100kJ"] || 0,
        nuti["蛋白质"]["每100mL"] || 0,
        nuti["蛋白质"]["每100g"] || 0
    ])
    // result[tyid] = {
    //     "脂肪": nuti["脂肪"]["每100g"],
    //     "蛋白质": nuti["蛋白质"]["每100g"],
    // }
}
fs.writeFileSync('../output-Task2.4.csv', result.map(x => x.join(",")).join("\n"), 'utf8')