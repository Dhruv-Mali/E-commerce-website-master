// CKEditor for Product Description
document.addEventListener('DOMContentLoaded', function() {
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.replace('id_description', {
            height: 400,
            toolbar: [
                { name: 'document', items: ['Source', '-', 'Preview'] },
                { name: 'clipboard', items: ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo'] },
                { name: 'editing', items: ['Find', 'Replace', '-', 'SelectAll'] },
                '/',
                { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'] },
                { name: 'paragraph', items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'] },
                { name: 'links', items: ['Link', 'Unlink'] },
                { name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'SpecialChar'] },
                '/',
                { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize'] },
                { name: 'colors', items: ['TextColor', 'BGColor'] },
                { name: 'align', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
                { name: 'tools', items: ['Maximize'] }
            ],
            removePlugins: 'elementspath',
            resize_enabled: false
        });
    }
});
