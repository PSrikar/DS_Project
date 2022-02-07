import React, { Component } from "react";
//import axios from 'axios'
//import PublisherList from "./PublishList";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Login from "./components/login.component";
import SignUp from "./components/signup.component";
import PublisherList from "./PublishList";
import Notifications from "./components/notifications.component";

export default class App extends Component {
  render() {
    return (
      // <>
      //   <div className="App">
      //     <h3 align="center">Pub-Sub Application</h3>
      //   </div>
      //   <div>
      //     <PublisherList />
      //   </div>
      // </>
      
      <Router>
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light fixed-top">
        <div className="container">
          <Link className="navbar-brand" to={"/sign-in"}>Meteorological Pub-Sub App</Link>
          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <Link className="nav-link" to={"/sign-in"}>Login</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={"/sign-up"}>Sign up</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to={"/notifications"}>Notifications</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="auth-wrapper">
        
          <Switch>
            <Route exact path='/' component={Login} />
            <Route path="/sign-in" component={Login} />
            <Route path="/sign-up" component={SignUp} />
            <Route exact path="/publishlist/:username" component={PublisherList} />
            <Route exact path="/notifications/:username" component={Notifications}/>
          </Switch>
        
      </div>
    </div></Router>

    );
  }
}
