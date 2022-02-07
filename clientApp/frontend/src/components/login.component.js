import React, { Component } from "react";
import axios from "axios";
//import { Route } from "react-router";
//import PublisherList from "../PublishList";
export default class Login extends Component {

    handleSubmit = (event) => {
        event.preventDefault()
        const subDetails = {
            username: event.target.username.value,
            password: event.target.password.value
        }
        try {
             axios.post('http://localhost:5000/api/login',{subDetails})
           .then(res=> {
            console.log(res)
            if(res.data === "OK")
            {
                alert('You have submitted the form.');
                window.location="/publishlist/:" + subDetails.username
            }
            if(res.data === "Failed")
            {
                alert("Username or Password is invalid")
                window.location="/"
            }
            
           })
           
           } catch (error) {
             console.log(error)
           }
    }



    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h3>Subscriber login</h3>

                <div className="form-group">
                    <label>Username</label>
                    <input type="text" name="username"  className="form-control" placeholder="Enter Username" />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input type="password" name="password" className="form-control" placeholder="Enter password" />
                </div>
                <div className="form-group">
                    <button type="submit"  className="btn btn-primary btn-block">Submit</button>
                </div>    
               
            </form>
        );
    }
}