function time_generator(){
    const xhr = new XMLHttpRequest()

    var input = document.getElementById("date-input").value
    
    if (!input){
        return
    }

    var date = new Date(input).toISOString().split('T')[0]

    xhr.open("POST", "/api/v1/occupied-time")
    xhr.setRequestHeader("Content-type", "application/json")
    xhr.send(JSON.stringify({"date": date}))

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)

            const bar = document.getElementById('bar')
            while (bar.lastChild) {
                bar.removeChild(bar.lastChild)
            }

            for (time of data.occupied_time) {
                const el = document.createElement('div')
                el.setAttribute('class', 'occupied-time')
                el.style.width = String((time[1] - time[0]) / 24 * 100) + '%'
                el.style.left = String(time[0] / 24 * 100) + '%'
                bar.appendChild(el)
            }
        }
    }
}


console.log('Hi');