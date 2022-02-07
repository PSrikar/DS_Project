import React, { Component } from "react";
import axios from "axios";
import Cards from "./cards.component";

export default class Notifications extends Component {
    constructor(props){
        super(props)
        this.state = {
         data: [],
         username:  this.props.match.params.username,
         notifications : [],
         brokerInfo: []
        }
      }
       
      getData(uname){
        axios.get('http://localhost:5000/api/notify',{ params: { username: this.props.match.params.username } }).then(res => {
        //   var data = JSON.parse(res.data)
          //this.setState({data:res.data})
          for(var i=0; i< res.data.length ; i++){
            this.setState({
              data: this.state.data.concat(res.data[i])
            });
          }

          console.log(res.data)
        })
      }

      getBrokerInfo(){
        axios.get('http://localhost:5000/api/subscribedBrokerInfo',{ params: { username: this.props.match.params.username } }).then(res => {
          console.log(res.data);
          //var brokerInfo = JSON.parse(res.data)
          this.setState({brokerInfo:res.data})
        })
      }

      getDataFromBrokerList(){
        console.log("In broker list function",this.state.brokerInfo)
        for(var i=0;i< this.state.brokerInfo.length;i++){
          console.log("broker",this.state.brokerInfo[i])
          var parsedData = this.state.brokerInfo[i]
          axios.get(parsedData.brokerAddress+'api/notify',{ params: { username: this.props.match.params.username } }).then(res=>{
            console.log("Data from brokers ",parsedData.brokerAddress);
            for(var i=0; i< res.data.length ; i++){
              this.setState({
                data: this.state.data.concat(res.data[i])
              });
            }
            console.log(res.data);
          })

        }
      }

      componentDidMount(){
        this.getBrokerInfo()
        //this.getData(this.props.match.params.username)
        //setInterval(this.getData.bind(this),30000)
        this.getDataFromBrokerList()
        setInterval(this.getDataFromBrokerList.bind(this),30000)
      }                

    clear = () => {
      for(var i=0; i< this.state.data.length ; i++){
        this.setState({
          data: this.state.data.slice(i,1)
        });
      }
    }

    CheckError= (props) =>{
      var data = props.obj;
      if(data.hasOwnProperty('error'))
      {
        return <p>{JSON.stringify(data)}</p>
      }
      else if(data.hasOwnProperty('data')){
        return <p>Elevation Data: {data.data.elevation}</p>
      }
    }
      
    render() {



        return(
          
           
            <>
            <div>
              
              {
                this.state.data.map((d,index) => (
                
                <>
                
                <p>{JSON.stringify(d)}</p>
                </>
              ))
              }
            </div>
            <div align="center">
              {this.state.data.length> 0 ? (<button onClick={this.clear}  className="btn btn-danger btn-block">Clear</button>) : (<h4>No notifications yet Hold ON!</h4>)}

            </div>
            <div>
             
            </div>
            </>   
        )
    }
}