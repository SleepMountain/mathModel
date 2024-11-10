import fs from 'fs';


const data = JSON.parse(fs.readFileSync('../output-WithRightUnit.json', 'utf8'));
const odata = {

}


for (let tyid in data) {
    let item = data[tyid];
    let apprs = item["【产品类别】"]
    if (odata[apprs] == undefined) {
        odata[apprs] = 0
    }
    odata[apprs] += 1
}
let o2data = {
    x:[],
    y:[]
}
//降序
Object.keys(odata).sort((a,b)=>odata[b]-odata[a]).forEach(key=>{
    o2data.x.push(key)
    o2data.y.push(odata[key])
})
console.log(o2data)
