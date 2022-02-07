import React ,{Component}  from "react";
import axios from 'axios'

export default class PublisherList extends Component {
    constructor(props){
        super(props)
        this.state = {
         data: []
        }
      }
    
      getData(){
        axios.get('http://localhost:5000/api/getPubs').then(res => {
          var data = JSON.parse(res.data)
         this.setState({data:data})
          
        })
      }
      componentDidMount(){
        this.getData()
      }

     subscribe = (indx) => {
       console.log("Pub Name",indx)
       console.log("Sub name",this.props.match.params.username)
       const pubsub = {pub_name:this.state.data[indx].name,sub_username:this.props.match.params.username}
       axios.put('http://localhost:5000/api/subscribe',{pubsub}).then(res => {
        var data = res.data
        alert('Subscription Successfull');
       }) 


     }

     unsubscribe = (indx) => {
      console.log("Pub Name",indx)
      console.log("Sub name",this.props.match.params.username)
      const pubsub = {pub_name:this.state.data[indx].name,sub_username:this.props.match.params.username}
      axios.delete('http://localhost:5000/api/unsubscribe',{data :  {pub_name:this.state.data[indx].name,sub_username:this.props.match.params.username}}).then(res => {
       var data = res.data
       alert(data);
      }) 
     }
     
     notifications = () =>{
       window.location = "/notifications/" + this.props.match.params.username
     }

    render() {
        console.log(this.state.data)
        return (
           <><div align="center">
            {this.state.data.map((d, indx) => (<><h4 key={indx}>Name: {d.name}</h4><button onClick={this.subscribe.bind(this, indx)}>Subscribe</button><button onClick={this.unsubscribe.bind(this, indx)}>UnSubscribe</button></>))}
          </div>
          <div align="center">
          <button onClick={this.notifications}  className="btn btn-primary btn-block">Notifications</button>
            </div></>  
        )
    }
}