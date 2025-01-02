async function handleLogout() {
    try {
        fetch('/auth/logout', {
            method: 'GET',
            credentials: 'include'
        })
            .then(res => res.json())
            .then(data => {
                console.log(data.message);
                // => 'Đăng xuất thành công'
                // Xoá localStorage, chuyển hướng v.v.
                window.location.href = '/';
            });
    } catch (error) {
        console.error(error);
        alert('Có lỗi xảy ra khi đăng xuất!');
    }
}