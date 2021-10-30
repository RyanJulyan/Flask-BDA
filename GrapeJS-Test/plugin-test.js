

grapesjs.plugins.add('test-plugin', function(editor, options){

    editor.DomComponents.addType('cutom-type', {
        isComponent: el => el.tagName == 'INPUT'
        ,model: {
            defaults: {
                traits: [
                    // Strings are automatically converted to text types
                     'name' // Same as: { type: 'text', name: 'name' }
                    ,'placeholder'
                    ,{
                        type: 'select' // Type of the trait
                        ,label: 'Type' // The label you will see in Settings
                        ,name: 'type' // The name of the attribute/property to use on component
                        ,options: [
                             {
                                  id: 'text'
                                 ,name: 'Text'
                             }
                            ,{
                                 id: 'email'
                                ,name: 'Email'
                             }
                            ,{
                                 id: 'password'
                                ,name: 'Password'
                             }
                            ,{
                                 id: 'number'
                                ,name: 'Number'
                             }
                        ]
                    },
                    {
                         type: 'checkbox'
                        ,name: 'required'
                    }
                ]
                // As by default, traits are binded to attributes, so to define
                // their initial value we can use attributes
                ,attributes: {
                     type: 'text'
                    ,required: true 
                }
            }
        }
    });
    
    editor.BlockManager.add('cutom-type-block', {
         label: 'Example Component'
        ,category: 'Example Group'
        // Select the component once it's dropped
        ,select: true
        ,draggable: false
        ,content: {
            type: 'cutom-type'
        }
    })
  
})