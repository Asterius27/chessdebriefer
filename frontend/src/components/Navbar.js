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
                <Link to="/">Players</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/compare">Compare</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/demo">Demo</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/endgames">Endgames</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/throws-comebacks">Throws-Comebacks (Slow)</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/accuracy">Accuracy (Slow)</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/openings">Openings</Link>
            </li>
            <li style={itemStyle}>
                <Link to="/upload">Upload PGN</Link>
            </li>
        </ul>
    </div>
    );
}

export default Navbar;