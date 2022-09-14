class WebChatController {
    constructor(view, model) {
        this.view = view
        this.model = model
        this.timer;
        this.xhttp;
        this.SERVER_TIME_OUT = 30000;
        this.URL = "https://af5d-139-47-73-138.eu.ngrok.io"
        this.END_POINT = "/webhooks/rest/webhook"

        this._initLocalListeners()
    }


    _initLocalListeners() {
        this.view.document.addEventListener(this.view.KEYUP, function(event) {
            if ((event.code === controller.view.INPUTPADENTER || event.code === controller.view.INPUTENTER) && controller.view.document.querySelector('#' + controller.view.ID_INPUTTEXT) === document.activeElement) {
                // Send Message
                controller.sendMessage()
            }
        });

        this.view.getElementById(this.view.ID_TOOGLE_CHAT).onclick = function () {
            controller.view.toggleWebChat()
        }

        this.view.getElementById(this.view.ID_BUTTON_SEND).onclick = function () {
            controller.sendMessage()
        }
    }

    sendMessage(text = null) {
        text = text == null ? this.view.getElementById(this.view.ID_INPUTTEXT).value : text
        if (text == "") { return }
        this.jannetTalk(text)
        this.view.writeInChat(this.view.chatResponses.user, text)
        this.view.writeInChat(this.view.chatResponses.boot, this.view.generateLoading())
        this.view.disableInputText()
        this.view.clearInput()
    }

    onTimeOut() {
        controller.xhttp.abort();
        controller.bootWriteChat("ERROR: Server is not responding...", true)
    }

    jannetTalk(question) {
        $('#rawChat').scrollTop($('#rawChat').height()*10);
        this.prepareXttp(question);
    }

    prepareXttp(question) {
        this.xhttp = new XMLHttpRequest();
        this.xhttp.open("POST", this.URL + this.END_POINT, true);
        this.xhttp.setRequestHeader("Content-Type", "application/json");
        this.timer = setTimeout(this.onTimeOut, this.SERVER_TIME_OUT);
        this.xhttp.onreadystatechange = function() {
            controller.model.serverResponse(this)
        };

        let data = {
            "sender" : this.view.MYID,
            "message" : question
        };

        console.log(question)
        this.xhttp.send(JSON.stringify(data));
    }

    bootWriteChat(text, error = false) {
        clearTimeout(this.timer);
        this.view.deleteLoagind()
        this.view.enableInputText()
        this.view.writeInChat(this.view.chatResponses.boot, text)
    }

    greetings() {
        this.sendMessage("Hola")
        let userMessages = this.view.getElementByClass("chat-right")
        userMessages[0].remove()
    }
}
let controller = new WebChatController(new WebChatView(document), new WebChatModel())
controller.greetings();