/* Project specific Javascript goes here. */
const url = `ws://${window.location.host}/ws/socket-server/`
const socket = new WebSocket(url)
let cur_dep_id = 0
let dep_emp = {}
let json
let data = {}
const departments = document.querySelectorAll('.collapse:not(.navbar-collapse)');


socket.onclose = (e) => {
    console.error(e);
}


// listen buttons and send request for new data if
// new department is shown
departments.forEach((department) => {
    department.addEventListener('shown.bs.collapse', function () {
        d = parseInt(department.id.replace(/[^0-9]/g,''))
        if (!(d in dep_emp)) {
            // department that hasn't opened before
            cur_dep_id = d
            socket.send(cur_dep_id)
            console.log(cur_dep_id)
        }
    })
})

function update_department(dep_id) {
    const department = document.getElementById(`collapse${dep_id}`)
    const ul = department.querySelector(':scope > div > ul')
    if (dep_emp[dep_id].length!=0 && dep_id in dep_emp) {
        for (const emp of dep_emp[dep_id]) {
            const li = document.createElement("li")
            const textnode = document.createTextNode(`${emp['last_name']} ${emp['first_name']} ${emp['patronic_name']}`)
            li.appendChild(textnode)
            ul.appendChild(li)
        }
    }
}

// for every messages from server
socket.addEventListener('message', (event) => {
    json = event.data.toString()
    data = JSON.parse(json)
    dep_emp[cur_dep_id] = JSON.parse(json)
    update_department(cur_dep_id)
})
