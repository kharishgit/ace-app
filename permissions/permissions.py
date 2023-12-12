from accounts.api.authhandle import AuthHandlerIns
from rest_framework.permissions import BasePermission
from accounts.models import Role, Permissions,User,NewQuestionPool
from rest_framework.exceptions import PermissionDenied
PERMISSIONSSTAF={
  "Category": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Level": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Course": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True,
        "Order_change":True
	
    },
    "Subject": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Module": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Topic": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "SubTopic": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Faculty": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Branch": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Batch": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "TimeTable":{
	    "create":False,
	    "edit":False,
	    "assignFaculty":True,
	    "delete":False,
	    "autoTimetable":True,
	    "photo":True
    },
    "Holiday": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Material": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "Download":True
    },
    "QuestionPool": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "Block":True,
        "PDF":True
    },
    "Attendance": { 
	    "create":True,
        "edit":True,
        "list":True,
        "delete":True,
        "PDF":True
    },
}

PERMISSIONADMIN={
    "create":True,
    "edit":True,
    "list":True,
    "delete":True,
    "Block":True
}

ROLES={
    "STAFF":PERMISSIONSSTAF,
    "ADMIN":PERMISSIONADMIN
}


class AdminAndRolePermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_role(request=request):
                roles = Role.objects.filter(user=AuthHandlerIns.get_id(request=request))
                for role in roles:
                    r = role.permissions.permissions
                    if r[view.permission][view.feature]:
                        return True
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
            elif AuthHandlerIns.is_staff(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except Exception as e:
            print(e,"e")
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        

class FacultyPermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_faculty(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        
class NonePermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        
class AdminOrStudent(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_student(request=request) or AuthHandlerIns.is_staff(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        
class OrPermission(BasePermission):
    status_code = 401
    def __init__(self, permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return any(permission().has_permission(request, view) for permission in self.permissions)
    

class StudentPermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_student(request=request):
                return True
            else:
                
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        

class AdminOrFaculty(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_faculty(request=request) or AuthHandlerIns.is_staff(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})


class AdminAndRoleOrFacultyPermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_role(request=request):
                roles = Role.objects.filter(user=AuthHandlerIns.get_id(request=request))
                for role in roles:
                    r = role.permissions.permissions
                    if r[view.permission][view.feature]:
                        return True
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})

            elif AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_faculty(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        

class AdminAndRolePermissionCopy(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        # try:

        if AuthHandlerIns.is_role(request=request):
            print("**")
            role = Role.objects.get(user=AuthHandlerIns.get_id(request=request))
            print(role,'kkkk')
            # print(role.permission,'lllllll')
            r = role.permissions.permissions
            print(r,'dd')
            # print(r[view.permission],'permissions')

            # print(r[view.permission],'permissions')
            print(r[view.permission][view.feature],'kkknnk')
            return r[view.permission][view.feature]
        elif AuthHandlerIns.is_staff(request=request):
            print('staff')
            return True
        elif AuthHandlerIns.is_faculty(request=request):
            print("((((((((((()))))))))))")
            if NewQuestionPool.objects.filter(user=AuthHandlerIns.get_id(request)):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        else:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        # except:
        #     return False

class AdminStudentFaculty(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_faculty(request=request) or AuthHandlerIns.is_staff(request=request) or AuthHandlerIns.is_student(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})

class StudentFacultyPermission(BasePermission):
    status_code = 401
    """
    A base class from which all permission classes should inherit.
    """
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if AuthHandlerIns.is_faculty(request=request) or AuthHandlerIns.is_student(request=request):
                return True
            else:
                raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})
        except:
            raise PermissionDenied({"message": "You do not have permission to access this resource.", "status_code": 401})

