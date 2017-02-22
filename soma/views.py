from django.contrib.auth import authenticate, login

def authenticate_view(rqst):
	if rqst.method == 'POST':
		username = rqst.POST['username']
		password = rqst.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			return login(request, user)
