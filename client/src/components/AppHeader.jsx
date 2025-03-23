// AppHeader component
export default function AppHeader() {

    const reloadPage = () => {
        window.location.reload();
    }

    return (
        <div className='title' onClick={reloadPage}>
            <img src="/coding.png" alt="DevBot" />
            <h2>DevBot</h2>
        </div>
    )
}
