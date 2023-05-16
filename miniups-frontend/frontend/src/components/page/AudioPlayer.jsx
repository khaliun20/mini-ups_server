import React from 'react';

class AudioPlayer extends React.Component {
  render() {
    return (
      <div>
        <audio controls>
          <source src={this.props.source} type="audio/mpeg" />
          Your browser does not support the audio tag.
        </audio>
      </div>
    );
  }
}

export default AudioPlayer;