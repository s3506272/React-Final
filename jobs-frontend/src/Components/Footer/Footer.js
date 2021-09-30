import { Link } from 'react-router-dom';

const Footer = (props) => {

    return (
        <footer className="footer mt-auto p-5">
            <Link className="text-white" to="/favourites?page=1" >View your favourites</Link>
        </footer >
    )
}

export default Footer;