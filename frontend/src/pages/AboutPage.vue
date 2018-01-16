<template>
  <v-container>
    <h2 class="my-3">Next Generation E-Voting Visualizer</h2>
    <p>This application is the result of the bachelor thesis "Visualizing Geneva's Next E-Voting System" and has been realized by <strong>Kevin Häni</strong> and <strong>Yannick Denzer</strong>.</p>
    <p>The full source code of this application is available on GitHub: <a href="https://github.com/nextgenevoting">https://github.com/nextgenevoting</a></p>
    <p>The "CHVote System Specifications" (the cryptographic specifications this application is based on), can be found here: <a href="https://eprint.iacr.org/2017/325">https://eprint.iacr.org/2017/325</a></p>

    <h3>About this application</h3>
    <p>With our application, it is possible to conduct election events according to the protocol specifications not only from the perspective of a voter, but also all other participating actors such as the election administrator, printing, or election authority, offering a preview of how the future of voting might possibly look like in Switzerland.</p>

    <h3>Context</h3>
    <p>Previous attempts to introduce e-voting platforms in Switzerland were limited to only small electorates as these platforms did only meet the basic requirements set up by the Swiss government. In 2017, researchers from the Research Institute for Security in the Information Society (RISIS) published their specifications for Geneva's new e-voting system, CHVote, which has the potential of being accepted as a large-scale, nationwide e-voting platform. However, one challenge that still remains is the educational problem: it is difficult to understand such a complex protocol without sufficient knowledge of cryptography. This might also result in mistrust towards e-voting.</p>

    <h3>Design and implementation</h3>
    <p>For this application we implemented approximately 60 algorithms that have been described in the specifications. This web application is powered using a back-end that implements the e-voting protocol by utilizing this crypto-library. Both the library as well as the back-end are written in Python. Our front-end that visualizes all the voting phases is a single-page application written in JavaScript using the VueJS framework. In order to achieve real-time updates, we have used web sockets (socket.io) to synchronize a client-side copy of the database whenever the data has been altered on the back-end.</p>
  </v-container>
</template>
