import fs from 'fs';


const data = JSON.parse(fs.readFileSync('../output-WithRightUnit.json', 'utf8'));
const listbyyear = {

}
for (let tyid in data) {
    let item = data[tyid];
    let year = item["【登记年份】"]
    if (listbyyear[year] == undefined) {
        listbyyear[year] = [0,0]
    }
    listbyyear[year][item["【产品来源】"] == "进口产品" ? 0 : 1] += 1
}   
const csvBody = []
const csvHeader = ["年份", "进口产品", "国产产品"]
for (let year in listbyyear) {
    csvBody.push([year, listbyyear[year][0], listbyyear[year][1]])
}
fs.writeFileSync('../output-Task2.1.csv', csvHeader.join(",") + "\n" + csvBody.map(x => x.join(",")).join("\n"), 'utf8')