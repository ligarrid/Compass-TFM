const ExcelWriter = require('./ExcelWriter')

run();

async function run() {
    console.log("SCRIPT INICIADO");

    await ExcelWriter.overWriteExcel()

    console.log("SCRIPT FIN");

}