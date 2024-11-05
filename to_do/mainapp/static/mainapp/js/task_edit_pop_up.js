document.addEventListener('DOMContentLoaded', () => {
    // Event delegation for adding tasks
    let addButton = document.querySelector('.add-task');
    if (addButton) {
        document.body.addEventListener('click', (event) => {
            if (event.target === addButton) {
                let addTaskPopup = document.querySelector('.add-task-popup');
                let addTaskPopupBg = document.querySelector('.add-ts-bg');
                if (addTaskPopup && addTaskPopupBg) {
                    addTaskPopup.classList.add('active');
                    addTaskPopupBg.classList.add('active');
                }
            }
        });
    }

    // Event delegation for closing add task popup
    let closeButtonAdd = document.querySelector('.close-button-addts');
    if (closeButtonAdd) {
        document.body.addEventListener('click', (event) => {
            if (event.target === closeButtonAdd) {
                let addTaskPopup = document.querySelector('.add-task-popup');
                let addTaskPopupBg = document.querySelector('.add-ts-bg');
                if (addTaskPopup && addTaskPopupBg) {
                    addTaskPopup.classList.remove('active');
                    addTaskPopupBg.classList.remove('active');
                }
            }
        });
    }

    // Event delegation for showing task details popup
    let tasks = document.getElementsByClassName('task');
    for (let i = 0; i < tasks.length; i++) {
        tasks[i].addEventListener('click', showPopup);
    }

    // Event delegation for closing task details popup
    let closeButtonEdd = document.querySelector('.close-button');
    if (closeButtonEdd) {
        document.body.addEventListener('click', (event) => {
            if (event.target === closeButtonEdd) {
                let popup = document.querySelector('.pop-up');
                let popupBg = document.querySelector('.pop-up-bg');
                if (popup && popupBg) {
                    popup.classList.remove('active');
                    popupBg.classList.remove('active');
                }
            }
        });
    }
    $("#team-select").on("change",(event)=>{
        $("#team-select-form").submit()
    })
});

function showPopup(event) {
    console.log(event.currentTarget.id);
    let popup = document.querySelector('.pop-up');
    let popupBg = document.querySelector('.pop-up-bg');
    let popupName = document.querySelector('.pop-up-name');
    if (popup && popupBg) {
        popup.classList.add('active');
        popupBg.classList.add('active');
        
        $.ajax({
            type: 'GET',
            url: `/tasks/${event.currentTarget.id}`,
            success: function(data){
                $('#id_id_edit').val(data['id']);
                $('#id_title_edit').val(data['title']);
                $('#id_text_edit').val(data['text']);
                $('#id_category_edit').val(data['category']);
                $('#id_status_edit').val(data['status']);
                $('#preview_img').attr('src', data['img']);
            }
        })
    }
}