class WebChatView {
    constructor(document) {
        this.ID_INPUTTEXT = 'text'
        this.ID_TOOGLE_CHAT = 'button-open-chat'
        this.ID_CHATCONTAINER = "chatContainer"
        this.ID_BUTTON_CLOSE = "button-open-chat-close"
        this.ID_BUTTON_OPEN = "button-open-chat-open"
        this.ID_RAW_CHAT = "rawChat"
        this.ID_BUTTON_SEND = "button_send";

        this.KEYUP = "keyup"
        this.INPUTARROWDOWN = "ArrowDown"
        this.INPUTENTER = "Enter"
        this.INPUTPADENTER = "NumpadEnter"
        this.INPUTARROWUP = "ArrowUp"

        this.document = document
        this.MYID = Math.floor(Date.now() / 1000)
        this.isTheLastMessage = true
        this.chatResponses = {
            boot: "left",
            user: "right",
        }
    }

    toggleWebChat() {
        let element = this.getElementById(this.ID_CHATCONTAINER);

        if (element.style.display === "none" || element.style.display === "") {
            this.unFadeWebChat(element)
        } else {
           this.fadeWebChat(element)
        }
    }

    fadeWebChat(element) {
        let close = this.getElementById(this.ID_BUTTON_CLOSE);
        let open = this.getElementById(this.ID_BUTTON_OPEN);

        close.style.display = "none"
        open.style.display = "inline-block";
        element.style.display = "none";

        let op = 1;  // initial opacity
        let timer = setInterval(function () {
            if (op <= 0.1){
                clearInterval(timer);
                element.style.display = 'none';
            }
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op -= op * 0.1;
        }, 10);
    }

    unFadeWebChat(element) {
        let close = this.getElementById(this.ID_BUTTON_CLOSE);
        let open = this.getElementById(this.ID_BUTTON_OPEN);

        close.style.display = "inline-block";
        open.style.display = "none";

        this.getElementById(this.ID_INPUTTEXT).focus()

        let op = 1;  // initial opacity
        element.style.display = 'block';
        let timer = setInterval(function () {
            if (op >= 1){
                clearInterval(timer);
            }
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op += op * 0.1;
        }, 10);
    }

    getElementById(id) {
        return this.document.getElementById(id)
    }

    getElementByClass(className) {
        return this.document.getElementsByClassName(className)
    }

    writeInChat(whoResponse, response, ERROR = false) {
        let alertPlaceholder = document.getElementById(this.ID_RAW_CHAT)
        alertPlaceholder.append(this.generateParraf(whoResponse, response, ERROR))
        $('#' + this.ID_RAW_CHAT).scrollTop($('#' + this.ID_RAW_CHAT).height()*10);
    }

    generateParraf(whoResponse, response, ERROR) {
        var div = document.createElement('div')
        var wrapper = document.createElement('p')
        var parrDate = document.createElement('p')

        var currentdate = new Date();
        var datetime = currentdate.getHours() + ":" + (currentdate.getMinutes()<10?'0':'') + currentdate.getMinutes();
        parrDate.innerHTML = datetime;
        div.append(wrapper)
        if (this.isTheLastMessage) { div.append(parrDate) }
        wrapper.className = " chatConver"; //@TODO: Cambiar esto
        wrapper.innerHTML = response;

        switch(whoResponse) {
            case this.chatResponses.boot:
                wrapper.className += " left";
                div.className = "chat-left";
                parrDate.className = "message-date-boot";
                break;
            case this.chatResponses.user:
                wrapper.className += " right";
                div.className = "chat-right";
                parrDate.className = "message-date-user";
                break;
        }

        if (ERROR) {
            wrapper.className += ' error-message';
        }

        return div
    }

    clearInput() {
        this.getElementById(this.ID_INPUTTEXT).value = "";
    }

    deleteLoagind() {
        const element = document.getElementById('loading');
        if (element == null) { return }
        document.getElementById("loading").parentElement.parentElement.remove()
    }

    generateCarrusel(array) {
        const idName = "accordion-" + Math.floor(Date.now() / 1000);
        var show = "show";
        console.log(array)
        var carrusel = '<div id="' + idName + '">';
        for (var i = 0; i < array.length; i++) {
            if (i >= 1) { show = "" }
            let item = array[i];
            let updated = item.updated.split('T');
            let name = item.name;
            let recordIdentifier = item.recordIdentifier;
            var isbn = "000";
            var isbnHTML = ""
            var isbnRaw = item.identifier;

            console.log(isbnRaw)
            if (isbnRaw != undefined) {
                isbn = isbnRaw.replace("urn:ISBN:", "");
                isbnHTML = "<small>ISBN : " + isbn + "</small><br>"
            }

            console.log(isbn)

            let title = item.title;
            let href = item.link.href;

            var imageURL = "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg";

            carrusel += '';
            carrusel += '\t\t\t\t\t\t\t<div class="card">\n' +
                '\t\t\t\t\t\t\t\t<div class="card-header" id="headingOne">\n' +
                '\t\t\t\t\t\t\t\t\t<h5 class="mb-0">\n' +
                '\t\t\t\t\t\t\t\t\t\t<button class="btn btn-link" data-toggle="collapse" data-target="#collapse' + recordIdentifier + '" aria-expanded="true" aria-controls="collapse' + recordIdentifier + '">\n' +
                '\t\t\t\t\t\t\t\t\t\t\t ' + title + '  \n' +
                '\t\t\t\t\t\t\t\t\t\t</button>\n' +
                '\t\t\t\t\t\t\t\t\t</h5>\n' +
                '\t\t\t\t\t\t\t\t</div>\n' +
                '\n' +
                '\t\t\t\t\t\t\t\t<div id="collapse' + recordIdentifier + '" class="collapse" aria-labelledby="headingOne" data-parent="#' + idName + '">\n' +
                '\t\t\t\t\t\t\t\t\t<div class="card-body" style="padding: 0rem 1rem;background: url(' + imageURL + ') no-repeat center #eee;">\n' +
                '\t\t\t\t\t\t\t\t\t\t<div class="card-deck">\n' +
                '\t\t\t\t\t\t\t\t\t\t\t<div class="card" style="background-color: rgb(255 255 255 / 85%);">\n' +
                '\t\t\t\t\t\t\t\t\t\t\t\t<div class="card-body">\n' +
                '\t\t\t\t\t\t\t\t\t\t\t\t\t<h5 class="card-title">' + name + '</h5>\n' +
                '\t\t\t\t\t\t\t\t\t\t\t\t\t<p class="card-text">' + isbnHTML +  '<small>OCLC ID : ' + recordIdentifier + '</small><br><small>Actualizado : ' + updated[0] + '</small></p>\n' +
                '\t\t\t\t\t\t\t\t\t\t\t\t\t<a target="_blank" href="' + href + '" class="card-text"><small class="text-muted">ver en catalogo</small></a>\n' +
                '\t\t\t\t\t\t\t\t\t\t\t\t</div>\n' +
                '\t\t\t\t\t\t\t\t\t\t\t</div>\n' +
                '\t\t\t\t\t\t\t\t\t\t</div>\n' +
                '\t\t\t\t\t\t\t\t\t</div>\n' +
                '\t\t\t\t\t\t\t\t</div>\n' +
                '\t\t\t\t\t\t\t</div>';
        }
        carrusel += "</div>";
        return carrusel;
    }

    static generateBootsrapDot() {
        return '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dot" viewBox="0 0 16 16">\n' +
            '  <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>\n' +
            '</svg>'
    }

    generateCard(carrusel, item, idName, show) {
        let name = item.name;
        let recordIdentifier = item.recordIdentifier;
        let itemUpdated = "1995-12-17T03:24:00";
        let isbn = "9788498381405"; // @TODO: CAMBIAR ESTO
        let title = item.title;
        let href = item.link.href;

        let imageURL = "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg";
        carrusel += '';
        carrusel += '\t\t\t\t\t\t\t<div class="card">\n' +
            '\t\t\t\t\t\t\t\t<div class="card-header" id="headingOne">\n' +
            '\t\t\t\t\t\t\t\t\t<h5 class="mb-0">\n' +
            '\t\t\t\t\t\t\t\t\t\t<button class="btn btn-link" data-toggle="collapse" data-target="#collapse' + recordIdentifier + '" aria-expanded="true" aria-controls="collapse' + recordIdentifier + '">\n' +
            '\t\t\t\t\t\t\t\t\t\t\t ' + title + '  \n' +
            '\t\t\t\t\t\t\t\t\t\t</button>\n' +
            '\t\t\t\t\t\t\t\t\t</h5>\n' +
            '\t\t\t\t\t\t\t\t</div>\n' +
            '\n' +
            '\t\t\t\t\t\t\t\t<div id="collapse' + recordIdentifier + '" class="collapse ' + show + '" aria-labelledby="headingOne" data-parent="#' + idName + '">\n' +
            '\t\t\t\t\t\t\t\t\t<div class="card-body" style="padding: 0rem 1rem;background: url(' + imageURL + ') no-repeat center #eee;">\n' +
            '\t\t\t\t\t\t\t\t\t\t<div class="card-deck">\n' +
            '\t\t\t\t\t\t\t\t\t\t\t<div class="card" style="background-color: rgb(255 255 255 / 85%);">\n' +
            '\t\t\t\t\t\t\t\t\t\t\t\t<div class="card-body">\n' +
            '\t\t\t\t\t\t\t\t\t\t\t\t\t<h5 class="card-title">' + name + '</h5>\n' +
            '\t\t\t\t\t\t\t\t\t\t\t\t\t<p class="card-text"><small>OCLC ID : ' + recordIdentifier + '</small></p>\n' +
            '\t\t\t\t\t\t\t\t\t\t\t\t\t<a target="_blank" href="' + href + '" class="card-text"><small class="text-muted">ver en catalogo</small></a>\n' +
            '\t\t\t\t\t\t\t\t\t\t\t\t</div>\n' +
            '\t\t\t\t\t\t\t\t\t\t\t</div>\n' +
            '\t\t\t\t\t\t\t\t\t\t</div>\n' +
            '\t\t\t\t\t\t\t\t\t</div>\n' +
            '\t\t\t\t\t\t\t\t</div>\n' +
            '\t\t\t\t\t\t\t</div>';

        return carrusel
    }

    generateLoading() {
        return '<div id="loading" class="spinner-border" role="status"><span class="sr-only"></span></div>'
    }


    disableInputText() {
        document.getElementById("text").readOnly = true;
        document.getElementById("text").placeholder = "Esperando respuesta";
    }

    enableInputText() {
        document.getElementById("text").readOnly = false;
        document.getElementById("text").placeholder = "Escribe aqui...";
    }
}