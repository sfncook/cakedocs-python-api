
def get_repo_name_from_url(repo_url):
    org = repo_url.split('/')[-2]
    proj = repo_url.split('/')[-1]
    return f"{org}/{proj}"