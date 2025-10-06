(function($) {
	$(document).ready(function($) {
        $('.field-verified').find('img[alt=False]').each(function() {
            var $this = $(this);
            $this.css("cursor", "pointer");
            $this.on('click', function() {
                if (confirm("You are going to set email as verified, are you sure?")) {
                    var email_id = $(this).closest("tr").find(".action-checkbox > .action-select").val();
					var url = '/en/admin/accounts/set_email_as_verified/' + email_id + '/';
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
