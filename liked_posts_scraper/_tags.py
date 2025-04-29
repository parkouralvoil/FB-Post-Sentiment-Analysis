from project_types import Tags

PostTags = Tags(
    _see_more_caption_class_tags = '', ## put the second tag of _text_tags here. No need to find see_more_caption div tags for posts
    _text_tags = '', 
    _secondary_text_tags = '',
    _container_tags = ''
)

VideoTags = Tags(
    _see_more_caption_class_tags = "",
    _text_tags = "",
    _secondary_text_tags = '',
    _container_tags = ''
)

PhotoTags = Tags(
    _see_more_caption_class_tags = "",
    _text_tags      = "",
    _secondary_text_tags = '',
    _container_tags = ""
)

## comments cannot be supported
# CommentTags = Tags(
#     _see_more_caption_class_tags = "",
#     _text_tags      = "",
#     _container_tags = ""
# )

ReelTags = Tags(
    _see_more_caption_class_tags = "",
    _text_tags = "",
    _secondary_text_tags = '',
    _container_tags = ""
)

# LiveVideoTags = Tags(
#     _see_more_caption_class_tags = "",
#     _text_tags = "",
#     _secondary_text_tags = '',
#     _container_tags = ""
# )

GroupTags = Tags(
    _see_more_caption_class_tags = "",
    _text_tags = "",
    _secondary_text_tags = '',
    _container_tags = "",
)

if __name__ == "__main__":
    print(PostTags.see_more_intersect_tags)
