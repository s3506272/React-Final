import './Header.css';
import { Search } from 'react-bootstrap-icons';
import { Link } from "react-router-dom";

const Header = (props) => {

    return (
        <header className="py-3 border-bottom">
            <Link to="/"> <h1> Job <Search /> <span>Search</span> </h1></Link>
        </header >
    )

}

export default Header;