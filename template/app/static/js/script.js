

$(document).ready(function(){
    $('.select2').select2({
        allowClear: true
      });
});

window.addEventListener("DOMContentLoaded", (e) => {
    $('select').on('select2:select', function (e) {
        $(this).closest('select').get(0).dispatchEvent(new Event('change'));
    });
});

add_key_value = document.getElementById('add_key_value')
var myScript = document.createElement("script");
key_value_input_count = 1

if(add_key_value){
    add_key_value.addEventListener('click',function(){
        let key_value_inputs = document.getElementById('key_value_inputs');
        key_value_inputs.innerHTML += `
        <div class="row border border-secondary rounded p-2 m-1" id="key_value_${key_value_input_count}">
            <div class="col-sm-5">
                <input type="text" class="form-control" name="key_${key_value_input_count}" id="key_${key_value_input_count}" placeholder="Key" autocomplete="key_${key_value_input_count}" >
            </div>
            <div class="col-sm-5">
                <input type="text" class="form-control" name="value_${key_value_input_count}" id="value_${key_value_input_count}" placeholder="Value" autocomplete="value_${key_value_input_count}" >
            </div>
            <div class="col-sm-2">
                <button type="button" class="form-control btn btn-block btn-danger" name="del_key_value_${key_value_input_count}" id="del_key_value_${key_value_input_count}"><i class="fa fa-trash"></i></button>
            </div>
        </div>`;

        myScript.innerHTML += `
del_key_value_${key_value_input_count} = document.getElementById('del_key_value_${key_value_input_count}')
del_key_value_${key_value_input_count}.addEventListener('click',function(){
    console.log('Clicked del_key_value_${key_value_input_count}')
    key_value_${key_value_input_count}.parentNode.removeChild(key_value_${key_value_input_count});
});
`
        key_value_inputs.appendChild(myScript);

        key_value_input_count++;
    });
}