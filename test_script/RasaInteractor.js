const axios = require('axios');

async function sendUtteranceToRasa(utt){

    return new Promise((resolve, reject) => {
        var data = JSON.stringify({
        "text": utt,
        "sender": "user"
        });

        var config = {
            method: 'post',
            url: 'http://localhost:5005/conversations/testing_conver/messages',
            headers: { 
                'Content-Type': 'application/json'
            },
            data : data
        };

        axios(config)
            .then(function (response) {
            // console.log(JSON.stringify(response.data));
            resolve(response.data) 
        })
            .catch(function (error) {
            console.log(error);
            reject(error)
        });
    })
}

module.exports.sendUtteranceToRasa = sendUtteranceToRasa