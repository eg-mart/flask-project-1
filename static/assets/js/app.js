function time_generator(){
    const xhr = new XMLHttpRequest()

    xhr.open("POST", "/api/v1/occupied-time", true)
    xhr.setRequestHeader("Content-type", "application/json")
    xhr.send('{"date":"2005-12-11"}')

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText)
            for (time of data.occupied_time) {
                const el = document.createElement('div')
                el.setAttribute('class', 'occupied-time')
                el.style.width = String((time[1] - time[0]) / 24 * 100) + '%'
                el.style.left = String(time[0] / 24 * 100) + '%'
                const bar = document.getElementById('bar')
                bar.appendChild(el)
            }
        }
    }
}


console.log('Hi');