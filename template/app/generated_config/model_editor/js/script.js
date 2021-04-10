

let groups = model_fields.groups

let current_models = Object.keys(all_models)

let html_values = ``;

for (let i in groups){
    let group = groups[i]
    
    html_values += field_templates.group_title(group);

    let elements = group.elements;

    if(i == 1){
        html_values += `
        <table class="table table-striped">
            <thead>
                <tr>
        `
        for(k in elements){
            let element = elements[k];

            html_values += `
                        <th>${element.title}</th>
            `
        }
        html_values += `
                </tr>
            </thead>
            <tbody id="field_rows">
                <tr>
        `;
    }

    for (j in elements){
        let element = elements[j];
        if(i != 1){
            html_values += (field_templates[element.type](element));
        }
    }

    if(i == 1){
        html_values += `
                </tr>
            </tbody>
        </table>
        `;
    }

}

$("#new_model_groups").html(html_values);


function create_field_row(group){

    let html_values = `<tr>`;
    
    let elements = group.elements;
    
    for (j in elements){
        let element = elements[j];
        html_values += (field_templates[element.type](element));
    }
    
    html_values += `</tr>`;
    
    $("#field_rows").append(html_values);
}

for (var i = 0; i<=2; i++){
    create_field_row(groups[1])
}