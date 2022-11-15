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
        }
    })
})

// update employer list of department
function update_department(dep_id) {
    const department = document.getElementById(`collapse${dep_id}`)
    if (dep_emp[dep_id].length!=0 && dep_id in dep_emp) {

        // Create card with subtitle and ul for pushing data
        const card = document.createElement('div')
        card.classList.add('card', 'card-body')
        department.prepend(card)

        const p = document.createElement('p')
        p.classList.add('h6', 'card-subtitle', 'mb-2', 'text-muted')
        const s = document.createTextNode('Сотрудники')
        p.appendChild(s)
        card.appendChild(p)

        const ul = document.createElement('ul')
        ul.classList.add('h6')
        card.appendChild(ul)

        for (const emp of dep_emp[dep_id]) {
            const li = document.createElement("li")
            const textnode = document.createTextNode(`${emp['last_name']} ${emp['first_name']} ${emp['patronic_name']}`)
            li.appendChild(textnode)
            ul.appendChild(li)
        }
    }
}

// listen for every message from server
socket.addEventListener('message', (event) => {
    json = event.data.toString()
    data = JSON.parse(json)
    dep_emp[cur_dep_id] = JSON.parse(json)
    update_department(cur_dep_id)
})
