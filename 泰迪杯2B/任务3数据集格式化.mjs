import fs from 'fs';

const CSVBody = []
let CSVHeader = ['注册证号', '有效期至', '产品类别', '组织状态', '适用人群', '适用人群类别', '产品来源', '登记年份']
const data = JSON.parse(fs.readFileSync('./output-WithRightUnitAndManualProofreading.json', 'utf8'));

const AllNutrition = []


for (let tyid in data) {
    let item = data[tyid];
    let nutris = item["【营养成分表】"]
    for (let nutri in nutris) {
        for (let unit in nutris[nutri]) {
            let fullname = nutri + "(" + unit + ")"
            if (AllNutrition.indexOf(fullname) == -1) {
                AllNutrition.push(fullname)
            }
        }
    }
}
CSVHeader = CSVHeader.concat(AllNutrition)

// fs.writeFileSync('./AllNuti.json', JSON.stringify(AllNutrition,null,4), 'utf8')

for (let tyid in data) {
    let item = data[tyid];
    let nuti = item["【营养成分表】"]
    let nutiArray = Array(AllNutrition.length).fill(0)
    for (let nutri in nuti) {
        for (let unit in nuti[nutri]) {
            let fullname = nutri + "(" + unit + ")"
            nutiArray[AllNutrition.indexOf(fullname)] = nuti[nutri][unit]
        }
    }
    CSVBody.push([tyid, item["【有效期至】"], item["【产品类别】"], item["【组织状态】"], item["【适用人群】"], item["【适用人群类别】"], item["【产品来源】"], item["【登记年份】"], ...nutiArray])

}

fs.writeFileSync('./TotalData.csv', CSVHeader.join("|") + "\n" + CSVBody.map(x => x.join("|")).join("\n"), 'utf8')