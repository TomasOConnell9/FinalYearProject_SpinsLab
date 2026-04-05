export default function Instructions() {
  return (
    <div>
      <h3>SpinsLab Instruction guide</h3>
      <p><strong>Welcome to SpinsLab!</strong></p>
      <p>Spinslab is an interactive simulation of the Stern-Gerlach experiment. Users can explore the behaviour of both spin-1/2 and spin-1 particles, perform experiments with multiple Stern-Gerlach analysers along any arbitrary axis and prepare their own unique quantum states.
        <br/><strong>Setup Instructions:</strong></p>
        <ul>
          <li>First select the desired spin type at the top of the page. 1/2 represents a spin-1/2 particle and 1 represents a spin-1 particle.</li>
          <li>Next use the "How many analysers" box to choose the amount of analysers you want present in the simulation.</li>
          <li>Configure the analysers along your desired axis by clicking the “Z” box on the analyser and selecting your preferred axis.
            <ul>
              <li>Selecting θ/φ allows you to set custom angles. Enter values in degrees directly, or click the π button to input radians.</li>
            </ul>
          </li>
          <li>You can send the particles from the source in a random state by selecting "R" in the source box or you can enter your own custom prepared quantum state by selecting "ψ".
            <ul>
          <li>If setting up a prepared quantum state, when you click on "ψ" you will be asked to enter the coefficients of the state.</li>
          <li>If the prepared state is not normalised, the simulation will normalise it for you. This will be indicated by a notification on the source box saying, "State normalised!".</li>
            </ul>
          </li>
          <li>To block any path click on either the up or down arrow on the analyser. This will change its colour from green to grey and remove the connecting line to the next box, indicating it is blocked.</li>
        </ul>
        <strong>Running Instructions:</strong>
        <ul>
          <li>Once the setup is configured as desired it is ready to run. First select how many particles you wish to simulate with designed experiment by change the number in the source box.</li>
          <li>To run the experiment you have two options. You can run the entirety of the particles in one go by pressing the "Run" button or you can run it one particle at a time using the "start" button.</li>
            <ul>
              <li>If you are running the experiment one particle at a time, you can control the speed of the particles using the speed dropdown menu on the source.</li>
              <li>If you are running in bulk, try not use too large values of particles as it will slow the simulation down for you.</li>
            </ul>
          <li>If you want to clear the experiment and start over simply press the rest button.</li>
        </ul>
        <strong>Experiments</strong>
        <p>To the right of the instruction guide, you will find a collection of experiments. These are designed for students who wish to explore key outcomes of the Stern–Gerlach experiment.</p>
</div>
  );
}