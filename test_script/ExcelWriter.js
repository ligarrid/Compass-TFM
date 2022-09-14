const Excel = require('exceljs');
const RasaInteractor = require('./RasaInteractor')
const path = './compass_test.xlsx';

async function overWriteExcel(){
    let excelbook = new Excel.Workbook();

    await excelbook.xlsx.readFile(path);
    let sheet = excelbook.getWorksheet(1);

    const rows = sheet.getRows(2, sheet.rowCount);

    for(let i = 0; i < rows.length; i++){
        let utt = rows[i].getCell(2).value
        console.log()
        if (utt != null){
            let response = await RasaInteractor.sendUtteranceToRasa(utt);
            console.log('Row ', i, 'Utterence ', utt)
            rows[i].getCell(5).value = response.latest_message.intent.name;
            rows[i].getCell(6).value = response.latest_message.intent.confidence;
            rows[i].getCell(9).value = response.latest_message.entities;

            rows[i].commit();
            await excelbook.xlsx.writeFile(path);
        }
    }


}

module.exports.overWriteExcel = overWriteExcel;