import React from 'react';
import { Link, NavLink } from 'react-router-dom';
//import './Nav.scss';
import 'styles/utils.scss'

const Nav = () => {
    return (
        /*
        <div className = "Nav">
            <NavLink exact to='/' className="item" activeClassName="activeStyle">Home</NavLink>
            <NavLink to='/workspace' className="item" activeClassName="activeStyle">Workspace</NavLink>
        </div>
        */
       /*
        <div className="nav">
            <ul id="nav-mobile">
                <NavLink exact to='/' className="left hide-on-med-and-down" activeClassName="active">Home</NavLink>
                <NavLink to='/workspace' className="left hide-on-med-and-down" activeClassName="active">Workspace</NavLink>
            </ul>
        </div>
        */




        /*
        <div>
            <div className="nav nav-extended">
                <div class="nav-wrapper">
                    <a href="#" class="brand-logo">Logo</a>
                    <a href="#" data-target="mobile-demo" class="sidenav-trigger"><i class="material-icons">menu</i></a>
                    <ul id="nav-mobile" class="right hide-on-med-and-down">
                        <li><a href="sass.html">Sass</a></li>
                        <li><a href="badges.html">Components</a></li>
                        <li><a href="collapsible.html">JavaScript</a></li>
                    </ul>
                </div>
                <div class="nav-content">
                    <ul class="tabs tabs-transparent">
                        <li class="tab"><a href="#test1">Test 1</a></li>
                        <li class="tab"><a class="active" href="#test2">Test 2</a></li>
                        <li class="tab disabled"><a href="#test3">Disabled Tab</a></li>
                        <li class="tab"><a href="#test4">Test 4</a></li>
                    </ul>
                </div>
            </div>

            <ul class="sidenav" id="mobile-demo">
                <li><a href="sass.html">Sass</a></li>
                <li><a href="badges.html">Components</a></li>
                <li><a href="collapsible.html">JavaScript</a></li>
            </ul>

            <div id="test1" class="col s12">Test 1</div>
            <div id="test2" class="col s12">Test 2</div>
            <div id="test3" class="col s12">Test 3</div>
            <div id="test4" class="col s12">Test 4</div>


        </div>
        */



        









        <div className="nav nav-extended">
            <div className="nav-wrapper">
                <Link exact to='/' className="brand-logo">Inspector Gadget</Link>
                <ul id="nav-mobile">
                    <Link to='/' className="right hide-on-med-and-down">Sign Up</Link>
                    <Link to='/' className="right hide-on-med-and-down">Sign In</Link>
                </ul>
            </div>
            
            <div className="nav-content">
                <ul className="tabs tabs-transparent">
                    <NavLink exact to='/' className="li tab" activeClassName="active"> Home </NavLink>
                    <NavLink to='/workspace' className="li tab" activeClassName="active"> Workspace </NavLink>
                </ul>
            </div>
        </div>            


        





        
        /*
        <div className = "Nav">
            <NavLink exact to='/' className="item" activeClassName="activeStyle">Home</NavLink>
            <NavLink to='/workspace' className="item" activeClassName="activeStyle">Workspace</NavLink>
        </div>
        */
    );
};

export default Nav;