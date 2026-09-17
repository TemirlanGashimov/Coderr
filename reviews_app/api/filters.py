from rest_framework.filters import BaseFilterBackend


class ReviewFilterBackend(BaseFilterBackend):
    """Filter reviews by the reviewed business or author."""

    def filter_queryset(self, request, queryset, view):
        business_user_id = request.query_params.get('business_user_id')
        reviewer_id = request.query_params.get('reviewer_id')
        if business_user_id:
            queryset = queryset.filter(business_user_id=business_user_id)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        return queryset