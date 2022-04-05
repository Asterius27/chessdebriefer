import { Link } from "react-router-dom";

const Navbar = () => {
    const navbarStyle = {
        width: "100%",
        display: "inline-block",
        margin: "auto"
    }

    const listStyle = {
        listStyle: "none",
        display: "inline-block",
    }

    const itemStyle = {
        display: "inline-block",
        marginLeft: "10px",
        marginRight: "10px"
    }

    return (
    <div style={navbarStyle}>
        <ul style={listStyle}>
            <li style={itemStyle}>
                <Link to="/">Percentages</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/upload">Upload PGN</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/players">Players</Link>
            </li>
        </ul>
    </div>
    );
}

export default Navbar;