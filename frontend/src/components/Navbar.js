import { Link } from "react-router-dom";
import { Navbar, Container, Nav } from "react-bootstrap";

const MyNavbar = () => {
    return (
        <Navbar bg="primary" variant="dark" expand="lg" sticky="top">
            <Container>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="m-auto">
                    <Nav.Link as={Link} to="/player">Players</Nav.Link>
                    <Nav.Link as={Link} to="/compare">Compare</Nav.Link>
                    <Nav.Link as={Link} to="/demo">Demo</Nav.Link>
                    <Nav.Link as={Link} to="/endgames">Endgames</Nav.Link>
                    <Nav.Link as={Link} to="/endgames/compare">Compare Endgames</Nav.Link>
                    <Nav.Link as={Link} to="/throws-comebacks">Throws-Comebacks (Slow)</Nav.Link>
                    <Nav.Link as={Link} to="/accuracy">Accuracy (Slow)</Nav.Link>
                    <Nav.Link as={Link} to="/openings">Openings</Nav.Link>
                    <Nav.Link as={Link} to="/upload">Upload PGN</Nav.Link>
                </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default MyNavbar;