
import course


def branchcopycourse(id, instance):
    print(id, "idddddddddddddddd")
    print(instance, "instaaaaaaaaaaaaaance")
    print(instance.courses.all(), "coursessssssssss")
    print(course.models.Branch.objects.filter(id=id).values('courses'))
    return


WEEKDAYS_CHOICES = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
)


def getchoicefromlist(arr):
    ans = []
    for i in range(0, 7):
        if arr[i]:
            ans.append(WEEKDAYS_CHOICES[i][0])
    print(ans)
    return ans



