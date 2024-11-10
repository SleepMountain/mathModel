import fs from 'fs';

const data = JSON.parse(fs.readFileSync('../output-WithRightUnit.json', 'utf8'));
const odata = {

}


for (let tyid in data) {
    let item = data[tyid];
    let appcs = item["【适用人群类别】"]
    let from = item["【产品来源】"]
    if (odata[appcs] == undefined) {
        odata[appcs] = {}
    }
    if (odata[appcs][from] == undefined) {
        odata[appcs][from] = 0
    }
    odata[appcs][from] += 1
}
console.log(odata)
