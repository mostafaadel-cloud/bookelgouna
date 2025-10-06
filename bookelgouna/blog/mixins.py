from blog.models import Category


class CategoriesToContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CategoriesToContextMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('translations')
        return context


class BlogPaginationMixin(object):
    def structure_pages(self, page_obj, paginator):
        pages = []
        current_page_idx = page_obj.number
        if paginator.num_pages >= 9:
            last_page_idx = paginator.num_pages
            last_3_pages_start_from = last_page_idx - 3
            prev_3_pages_of_curr_from_idx = current_page_idx - 3
            next_3_pages_of_curr_to_idx = current_page_idx + 3
            for idx in paginator.page_range:
                if idx < 4 or idx > last_3_pages_start_from or \
                        (prev_3_pages_of_curr_from_idx - 1 <= idx <= next_3_pages_of_curr_to_idx + 1):
                    page = {}
                    page['active'] = idx == current_page_idx
                    if (idx == prev_3_pages_of_curr_from_idx - 1 and idx > 3) or \
                            (idx == next_3_pages_of_curr_to_idx + 1 and idx <= last_3_pages_start_from):
                        page['dots'] = True
                    else:
                        page['idx'] = idx
                    pages.append(page)
        else:
            # if there is small pages number then nothing to do here except active page setting
            for idx in paginator.page_range:
                page = {
                    'active': idx == current_page_idx,
                    'idx': idx
                }
                pages.append(page)
        return pages