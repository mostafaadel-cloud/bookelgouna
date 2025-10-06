(function($) {
	$(document).ready(function($) {
        $('.field-is_active').find('img[alt=True]').each(function() {
            var $this = $(this);
            $this.css("cursor", "pointer");
            $this.on('click', function() {
                if (confirm("You are going to deactivate a user, are you sure?")) {
                    var user_id = $(this).closest("tr").find(".action-checkbox > .action-select").val();
					var url = '/en/admin/accounts/deactivate/' + user_id + '/';
                    $.post(url, {}, function(resp) {
                        if ('status' in resp) {
                            if (resp['status'] === 'fail') {
                                alert(resp['message']);
                            } else if (resp['status'] === 'success') {
                                location.reload(true);
                            }
                        }
                    });
                }
            });
        });
	});
})(django.jQuery);
