
let local_db
local_db = ImmortalDB.ImmortalDB


$(document).ready(function(){
    $('.select2').select2({
        allowClear: true
    });

    $('.daterangepicker_single').daterangepicker({
      singleDatePicker: true,
      timePicker: true,
      timePickerIncrement: 15,
      timePicker24Hour: true,
      showISOWeekNumbers: true,
      locale: {
        format: 'YYYY-MM-DD HH:mm'
      }
    })

    $('.daterangepicker_range').daterangepicker({
      singleDatePicker: false,
      timePicker: true,
      timePickerIncrement: 15,
      timePicker24Hour: true,
      showISOWeekNumbers: true,
      locale: {
        format: 'YYYY-MM-DD HH:mm'
      }
    })
});

window.addEventListener("DOMContentLoaded", (e) => {
    $('select').on('select2:select', function (e) {
        $(this).closest('select').get(0).dispatchEvent(new Event('change'));
    });
});


////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////// generic_key_value /////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

data_types = [
    {
        "data_type":"text",
        "name":"Text"
    },
    {
        "data_type":"number",
        "name":"Number"
    },
    {
        "data_type":"checkbox",
        "name":"Tick box"
    },
    {
        "data_type":"password",
        "name":"Password"
    },
    {
        "data_type":"color",
        "name":"Color"
    },
    {
        "data_type":"email",
        "name":"Email"
    },
    {
        "data_type":"range",
        "name":"Slider"
    },
    {
        "data_type":"file",
        "name":"File"
    }
]


function return_inout_option(key_value){
    const inout_options = {
        'text':`<input type="text" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'number':`<input type="number" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'checkbox':`<input type="checkbox" class="form-control" checked="${key_value.value? key_value.value : 'false'}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'password':`<input type="password" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'color':`<input type="color" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'email':`<input type="email" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'range':`<input type="range" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`,
        'file':`<input type="file" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}')" >`
    }

    return inout_options[key_value.data_type];
}


function return_template(key_value,data_types = data_types){

    const template = `
        <div class="row border border-secondary rounded p-2 m-1" id="key_value_${key_value.id}_group">
            <div class="col-sm-4">
                <input type="text" class="form-control" value="${key_value.key? key_value.key : ''}" name="key_${key_value.id}" id="key_${key_value.id}" placeholder="Key" autocomplete="key_${key_value.id}" onchange="update_key_value('${key_value.id}')" >
            </div>
            <div class="col-sm-2">
                <select class="select2 form-control" name="selector_${key_value.id}" id="selector_${key_value.id}" data-placeholder="Choose Data Type" autocomplete="selector_${key_value.id}" onchange="update_key_value('${key_value.id}')" >
                    <option aria-readonly="true" readonly="true" disabled="true" selected="true">Choose Data Type</option>
                    ${data_types.map(data_type => `<option value="${data_type.data_type}" ${(key_value.data_type == data_type.data_type)? "selected='true'" : ''}>${data_type.name}</option>`).join("")}
                </select>
            </div>
            <div class="col-sm-4">
                ${return_inout_option(key_value)}
            </div>
            <div class="col-sm-2">
                <button type="button" class="form-control btn btn-block btn-danger" name="del_key_value_${key_value.id}" id="del_key_value_${key_value.id}" onclick="delete_key_value('${key_value.id}')"><i class="fa fa-trash"></i></button>
            </div>
        </div>`;

    return template;

}


async function get_generic_key_value(generic_key = 'generic_key_value'){
	let generic_key_value = await local_db.get(generic_key);
    if(isEmpty(generic_key_value)){
        generic_key_value = []
    }
    else{
        generic_key_value = JSON.parse(generic_key_value)
    }
	return generic_key_value;
}


async function set_generic_key_value(key_value, generic_key = 'generic_key_value'){
    key_value = JSON.stringify(key_value)
	let generic_key_value = await local_db.set(generic_key, key_value);
	return JSON.parse(generic_key_value);
}


async function remove_generic_key_value_id(id, generic_key = 'generic_key_value'){
    let key_val = [];
	// let generic_key_val = await get_generic_key_value(generic_key);
	let generic_key_val = await get_generic_key_value(generic_key);

	let key_val_index = generic_key_val.findIndex(function (kv){
        return kv.id = id; // [{id:1},{id:2}]
    });
	
	if (key_val_index > -1){
        generic_key_val.splice(key_val_index, 1);
        key_val = await set_generic_key_value(generic_key_val);
    }
    else{
        key_val = await get_generic_key_value();
    }

}


async function remove_all_generic_key_values(generic_key = 'generic_key_value'){
    await local_db.remove(generic_key);

	let generic_key_value = await get_generic_key_value(generic_key);
    return generic_key_value;
}


async function render_generic_key_value(element = document.getElementById('key_value_inputs'), generic_key = 'generic_key_value'){
	let generic_key_value = await get_generic_key_value(generic_key);
	element.innerHTML = '';

	for (let key_value in generic_key_value){
        element.innerHTML += return_template(generic_key_value[key_value], data_types);
	}
	
}


async function add_key_value(generic_key = 'generic_key_value'){

    let id = uuidv4();
    let key = '';
    let data_type = 'text';
    let value = '';
	
    let generic_key_val = await new_key_value(
        id,
        key,
        data_type,
        value,
        generic_key
    )

    element = document.getElementById('key_value_inputs')

    render_generic_key_value(element, generic_key);

}


async function delete_key_value(id, generic_key = 'generic_key_value'){

    await remove_generic_key_value_id(id)

    element = document.getElementById('key_value_inputs')

    render_generic_key_value(element, generic_key);

}


async function new_key_value(id, key = '', data_type = '', value = '', generic_key = 'generic_key_value'){

	let generic_key_value = await get_generic_key_value(generic_key);

    let data = {
        "id":id,
        "key":key,
        "data_type":data_type,
        "value":value
    }
    
    generic_key_value.push(data);

    generic_key_val = await set_generic_key_value(generic_key_value);

	return generic_key_val;

}


async function update_key_value(id,generic_key = 'generic_key_value'){
    await remove_generic_key_value_id(id,generic_key);
    
    let key_element = document.getElementById("key_"+id);
    let selector_element = document.getElementById("selector_"+id);
    let value_element = document.getElementById("value_"+id);

    let key = key_element.value;
    let data_type = selector_element.value;
    let value = value_element.value;

    if(value_element.type == 'checkbox'){
        value = value_element.checked
    }
    
    key_element.removeAttribute("value");
    selector_element.removeAttribute("value");
    value_element.removeAttribute("value");
    
    key_element.value = key;
    selector_element.value = data_type;
    value_element.value = value;
    
    key_element.defaultValue = key;
    selector_element.defaultValue = data_type;
    value_element.defaultValue = value;
    
    key_element.setAttribute('value', key);
    selector_element.setAttribute('value', data_type);
    value_element.setAttribute('value',value);
    
    let generic_key_val = await new_key_value(
                                                id,
                                                key,
                                                data_type,
                                                value,
                                                generic_key
                                            )

	return generic_key_val;
}

let generic_key = 'generic_key_value'
let element = document.getElementById('key_value_inputs')

if(element){
    render_generic_key_value(element, generic_key);
}

const add_key_value_btn = document.getElementById('add_key_value')
if(add_key_value_btn){
    add_key_value_btn.addEventListener('click',async function(){
        await add_key_value();
    });
}

