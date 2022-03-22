
let local_db
// local_db = ImmortalDB.ImmortalDB


$(document).ready(function(){
    $('.select2').select2({
        allowClear: true
    });

    htmx.logger = function(elt, event, data) {
        if(event == 'htmx:afterRequest'){
            console.log(data.xhr.status);
            $('#results_status').val(data.xhr.status);
        }
        // if(console) {
        //     console.log(event, elt, data.xhr);
        // }
    }

    htmx.on('htmx:responseError', function(event) { 
        $('#results').html(event.detail.xhr.responseText)
    });

    $('.daterangepicker_single').daterangepicker({
      singleDatePicker: true,
      timePicker: true,
      timePickerIncrement: 15,
      timePicker24Hour: true,
      showISOWeekNumbers: true,
      locale: {
        format: 'YYYY-MM-DD HH:mm:ss'
      }
    });

    $('.daterangepicker_range').daterangepicker({
      singleDatePicker: false,
      timePicker: true,
      timePickerIncrement: 15,
      timePicker24Hour: true,
      showISOWeekNumbers: true,
      locale: {
        format: 'YYYY-MM-DD HH:mm:ss'
      }
    });

    $('.deleteModalBtn').on("click", function (e) {
        var newUrl =  $(this).data('link');
        $('.deleteRecordBtn').attr("href", newUrl);
   });

   $('.DataTable').DataTable({
        'paging'      : true,
        'responsive'  : false,
        'lengthChange': true,
        'searching'   : true,
        'ordering'    : true,
        'info'        : true,
        'fixedHeader' : true,
        'colReorder'  : true,
        'autoWidth'   : false,
        "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
        "pageLength": 10,
        "dom": 'Bfrtip',
        'buttons'	  : [
            'pageLength',
            'colvis',
            {
                extend: 'copy',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'csv',
                exportOptions: {
                    columns: ':visible'
                }
            },
            'excelHtml5',
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'print',
                exportOptions: {
                    columns: ':visible'
                }
            }
        ],
        language: {
                buttons: {
                pageLength: '%d'
                ,colvis: 'Columns'
            }
        }
    });
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
        "data_type":"date",
        "name":"Date"
    },
    {
        "data_type":"daterange",
        "name":"Date Range"
    },
    {
        "data_type":"datetime",
        "name":"Date & time"
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
        "data_type":"select",
        "name":"Dropdown"
    },
    {
        "data_type":"file",
        "name":"File"
    }
]


function return_input_option(key_value, data=[], key_value_input){
    let json_data = JSON.stringify(data);
    json_data = encodeURI(json_data)
    
    const inout_options = {
        'text':`<input type="text" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'number':`<input type="number" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'date':`<input type="text" class="form-control daterangepicker_single" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'daterange':`<input type="text" class="form-control daterangepicker_single" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'datetime':`<input type="text" class="form-control daterangepicker_single" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'checkbox':`<input type="checkbox" class="form-control" ${key_value.value == true? 'checked="true"' : ''}" value="${key_value.value? key_value.value : 'false'}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'password':`<input type="password" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'color':`<input type="color" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'email':`<input type="email" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'range':`<input type="range" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`,
        'select':`<select class="form-control" name="value_${key_value.id}" id="value_${key_value.id}" data-placeholder="Choose Option" autocomplete="selector_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}', '${json_data}')" >
            <option aria-readonly="true" readonly="true" disabled="true" selected="true">Choose Option</option>
            ${data.map(val => `<option value="${val.id}" ${(key_value.value == val.id)? "selected='true'" : ''}>${val.name}</option>`).join("")}
        </select>`,
        'file':`<input type="file" class="form-control" value="${key_value.value? key_value.value : ''}" name="value_${key_value.id}" id="value_${key_value.id}" placeholder="Value" autocomplete="value_${key_value.id}" onchange="update_key_value('${key_value.id}', '${key_value_input}', '${generic_key}')" >`
    }

    return inout_options[key_value.data_type];
}


function return_template(key_value, data, key_value_input, data_types = data_types, element_id, generic_key){
    let json_data = JSON.stringify(data);
    json_data = encodeURI(json_data)

    const template = `
        <div class="row border border-secondary rounded p-2 m-1" id="key_value_${key_value.id}_group">
            <div class="col-sm-4">
                <input type="text" class="form-control" value="${key_value.key? key_value.key : ''}" name="key_${key_value.id}" id="key_${key_value.id}" placeholder="Key" autocomplete="key_${key_value.id}" onchange="update_key_value('${key_value.id}', '${json_data}', '${generic_key}')" >
            </div>
            <div class="col-sm-2">
                <select class="form-control" name="selector_${key_value.id}" id="selector_${key_value.id}" data-placeholder="Choose Data Type" autocomplete="selector_${key_value.id}" onchange="update_key_value('${key_value.id}', '${json_data}', '${generic_key}')" >
                    <option aria-readonly="true" readonly="true" disabled="true">Choose Data Type</option>
                    ${data_types.map(data_type => `<option value="${data_type.data_type}" ${(key_value.data_type == data_type.data_type)? "selected='true'" : ''}>${data_type.name}</option>`).join("")}
                </select>
            </div>
            <div class="col-sm-4">
                ${return_input_option(key_value, data, key_value_input)}
            </div>
            <div class="col-sm-2">
                <button type="button" class="form-control btn btn-block btn-danger" name="del_key_value_${key_value.id}" id="del_key_value_${key_value.id}" onclick="delete_key_value('${key_value.id}', '${element_id}', '${generic_key}')"><i class="fa fa-trash"></i></button>
            </div>
        </div>`;

    return template;

}


function get_generic_key_value(generic_key){
	// let generic_key_value = await local_db.get(generic_key);
	let generic_key_value = localStorage.getItem(generic_key);
    if(isEmpty(generic_key_value)){
        generic_key_value = {}
    }
    else{
        generic_key_value = JSON.parse(generic_key_value)
    }
	return generic_key_value;
}


function set_generic_key_value(key_value, generic_key){
    key_value = JSON.stringify(key_value)
	// let generic_key_value = await local_db.set(generic_key, key_value);
	localStorage.setItem(generic_key, key_value);
	let generic_key_value = get_generic_key_value(generic_key);
	return generic_key_value;
}


function remove_generic_key_value_id(id, generic_key){
    let key_val = {};
	// let generic_key_val = await get_generic_key_value(generic_key);
	let generic_key_val = get_generic_key_value(generic_key);
	
	if (id in generic_key_val){
        delete generic_key_val[id]
        key_val = set_generic_key_value(generic_key_val, generic_key);
    }

}


function remove_all_generic_key_values(generic_key){
    // await local_db.remove(generic_key);
    localStorage.removeItem(generic_key);

	let generic_key_value = get_generic_key_value(generic_key);
    return generic_key_value;
}


function render_generic_key_value(element, data, key_value_input, element_id, generic_key){
    let generic_key_value = get_generic_key_value(generic_key);
	element.innerHTML = '';

	for (let key_value in generic_key_value){
        element.innerHTML += return_template(generic_key_value[key_value], data, key_value_input, data_types, element_id, generic_key);
	}
    
    setTimeout(function(){

        $('.daterangepicker_single').daterangepicker({
          singleDatePicker: true,
          timePicker: true,
          timePickerIncrement: 15,
          timePicker24Hour: true,
          showISOWeekNumbers: true,
          locale: {
            format: 'YYYY-MM-DD HH:mm'
          }
        });

        $('.daterangepicker_range').daterangepicker({
          singleDatePicker: false,
          timePicker: true,
          timePickerIncrement: 15,
          timePicker24Hour: true,
          showISOWeekNumbers: true,
          locale: {
            format: 'YYYY-MM-DD HH:mm'
          }
        });
    });
}

function add_key_value(element_id, key_value_input, generic_key, default_key = '', default_data_type = 'text', data = [], default_value = ''){

    let id = uuidv4();
    let key = default_key;
    let data_type = default_data_type;
    let value = default_value;
	
    let generic_key_val = new_key_value(
        id,
        key,
        data_type,
        value,
        generic_key
    )

    element = document.getElementById(element_id)

    render_generic_key_value(element, data, key_value_input, element_id, generic_key);

}


function delete_key_value(id, element_id, generic_key){
    
    remove_generic_key_value_id(id, generic_key)
    
    element = document.getElementById(element_id)
    
    render_generic_key_value(element, data, key_value_input, element_id, generic_key);

}


function new_key_value(id, key = '', data_type = '', value = '', generic_key){

	let generic_key_value = get_generic_key_value(generic_key);

    let data = {
        "id":id,
        "key":key,
        "data_type":data_type,
        "value":value
    }
    
    generic_key_value[id] = (data);

    generic_key_val = set_generic_key_value(generic_key_value, generic_key);

	return generic_key_val;

}


function update_key_value(id, key_value_input, generic_key, data = []){

    if(typeof data == 'string'){
        data = JSON.parse(decodeURI(data))
    }

    remove_generic_key_value_id(id,generic_key);
    
    let key_value_input = document.getElementById(key_value_input);
    let key_element = document.getElementById("key_"+id);
    let selector_element = document.getElementById("selector_"+id);
    let value_element = document.getElementById("value_"+id);

    let key = key_element.value;
    let data_type = selector_element.value;
    let value = value_element.value;

    if(value_element.type == 'checkbox'){
        value = value_element.checked;
    }
    
    key_value_input.removeAttribute("value");
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
    
    value_element.parentElement.innerHTML = return_input_option({
                                                    "id":id,
                                                    "key":key,
                                                    "data_type":data_type,
                                                    "value":value
                                                },
                                                data);
    
    let generic_key_val = new_key_value(
                                                id,
                                                key,
                                                data_type,
                                                value,
                                                generic_key
                                            )

    key_value_input.value = JSON.stringify(generic_key_val);
    key_value_input.defaultValue = JSON.stringify(generic_key_val);
    key_value_input.setAttribute('value', JSON.stringify(generic_key_val));
    
    setTimeout(function(){

        $('.daterangepicker_single').daterangepicker({
          singleDatePicker: true,
          timePicker: true,
          timePickerIncrement: 15,
          timePicker24Hour: true,
          showISOWeekNumbers: true,
          locale: {
            format: 'YYYY-MM-DD HH:mm'
          }
        });

        $('.daterangepicker_range').daterangepicker({
          singleDatePicker: false,
          timePicker: true,
          timePickerIncrement: 15,
          timePicker24Hour: true,
          showISOWeekNumbers: true,
          locale: {
            format: 'YYYY-MM-DD HH:mm'
          }
        });
    });

	return generic_key_val;
}

let element = document.getElementById('key_value_inputs')

if(element){
    let generic_key = 'generic_key_value'
    let data = []
    let key_value_input = 'key_value'
    render_generic_key_value(element, data, key_value_input, element_id, generic_key);
}

const add_key_value_btn = document.getElementById('add_key_value')
if(add_key_value_btn){
    add_key_value_btn.addEventListener('click',function(){
        add_key_value(element_id = 'key_value_inputs', key_value_input = 'key_value', generic_key = 'generic_key_value');
    });
}

