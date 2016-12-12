React = require "react"
_ = require "underscore"
ReactDOM = require "react-dom"
FontAwesome = require "react-fontawesome"

ExampleInterface = React.createClass

    getDefaultProps: ->
        return {}

    getInitialState: ->
        return {
        }

    componentWillUnmount: ->
        return

    componentDidMount: ->
        return

    shouldComponentUpdate: (nextProps, nextState) ->
        if not _.isEqual(@state, nextState)
            return true
        return false

    render: ->
        return (<div><span>Hello React-Coffee!</span></div>)


mountedInterface = ReactDOM.render(<ExampleInterface/>, document.getElementById("your-mount-point"))