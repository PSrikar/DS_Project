import React, { Component } from "react";
import axios from "axios";
export default class SignUp extends Component {

    handleSubmit = (event) => {
        event.preventDefault()
        const subDetails = {
            name: event.target.name.value,
            email: event.target.email.value,
            username: event.target.username.value,
            pwd: event.target.password.value
        }

        try{
            axios.put('http://localhost:5000/api/createSubs',{subDetails})
            .then(res=>{
                alert('Subscriber created successfully');
                window.location="/"
            })
        }catch(error){
            console.log(error)
        }

    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <h3>Sign Up</h3>

                <div className="form-group">
                    <label>Name</label>
                    <input type="text" name="name" className="form-control" placeholder="First name" />
                </div>

                <div className="form-group">
                    <label>Email address</label>
                    <input type="email" name="email" className="form-control" placeholder="Enter email" />
                </div>

                <div className="form-group">
                    <label>Username</label>
                    <input type="text" name="username" className="form-control" placeholder="Enter Username" />
                </div>

                <div className="form-group">
                    <label>Password</label>
                    <input type="password" name="password" className="form-control" placeholder="Enter password" />
                </div>

                <button type="submit" className="btn btn-primary btn-block">Sign Up</button>

            </form>
        );
    }
}