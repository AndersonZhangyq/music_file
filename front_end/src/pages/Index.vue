<template>
  <q-page>
    <div class="q-pa-md">
      <div class="row text-subtitle1">Please choose your file type</div>
      <div class="row">
        <q-uploader
          url="apis/upload"
          label="WAV and MP3 file are accepted"
          accept=".wav, .mp3"
          @rejected="onRejected"
          @added="onAdded"
        />
      </div>
      <div v-if="duration > 0">
        <div class="row q-pt-sm text-body1">
          Your audio file is about <b>&nbsp;{{ duration }}&nbsp;</b> seconds
          long
        </div>
        <div class="row">
          <q-input
            v-model="time_gap"
            type="number"
            lazy-rules
            :rules="[
              (val) => (val !== null && val !== '') || 'Please type time gap',
              (val) => val > 0 || 'The time gap should be positive',
            ]"
            style="min-width: 30em"
            label="Please type the time gap you prefer to have"
            suffix="seconds"
          />
        </div>
        <div class="row text-body1" v-if="num_intact > 0 || num_non_intact > 0">
          Your audio file will be cut into
          <b>&nbsp;{{ num_intact }}&nbsp;</b> intact parts. The rest non-intact
          part contains <b>&nbsp;{{ num_non_intact }}&nbsp;</b> seconds
        </div>
        <div class="row text-subtitle1 q-pt-sm">
          Please choose the picture you want to output:
        </div>
        <div class="row">
          <q-option-group
            v-model="pictures"
            type="checkbox"
            :options="picture_options"
            color="primary"
            inline
          />
        </div>
        <div class="row">
          <q-btn label="Submit" color="primary" @click="submit"></q-btn>
        </div>
        <div
          :class="{
            row: true,
            'q-pt-sm': true,
            'justify-center': image_loading,
          }"
        >
          <q-spinner-hourglass color="purple" size="4em" v-if="image_loading" />
          <viewer
            :options="viewer_options"
            :images="output_images"
            ref="viewer"
            v-if="output_images.length > 0"
          >
            <template slot-scope="scope">
              <div
                v-for="{ src, alt } in scope.images"
                :key="src"
                style="display: inline-block"
              >
                <img
                  :src="src"
                  :alt="alt"
                  style="
                    height: 200px;
                    cursor: pointer;
                    margin: 5px;
                    display: inline-block;
                  "
                />
                <div class="text-subtitle1 text-center">{{ alt }}</div>
              </div>
            </template>
          </viewer>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import "viewerjs/dist/viewer.css";
import Viewer from "v-viewer/src/component.vue";
export default {
  components: {
    Viewer,
  },
  name: "PageIndex",
  methods: {
    submit: function () {
      if (this.time_gap == null) {
        this.$q.notify({
          type: "negative",
          message: "Please type the time gap",
        });
        return;
      }
      if (this.pictures.length == 0) {
        this.$q.notify({
          type: "negative",
          message: "Please select the picture",
        });
        return;
      }
      let send_obj = {
        gap_val: this.time_gap,
        pictures: this.pictures,
      };
      console.log(send_obj);
      this.output_images = [];
      this.image_loading = true;
      fetch("apis/submit", {
        method: "POST",
        body: JSON.stringify(send_obj),
      })
        .then((response) => response.json())
        .then((data) => {
          // this.output_images = [
          //   {
          //     src: "https://cdn.quasar.dev/img/mountains.jpg",
          //     alt: "mountain",
          //   },
          //   {
          //     src:
          //       "https://d33wubrfki0l68.cloudfront.net/28e392e11daadef180e12e890014c81dec12bd0c/3738d/image-4.a4d08f7d.jpg",
          //     alt: "cat",
          //   },
          // ];
          this.output_images = data;
          this.image_loading = false;
        })
        .catch(() => {
          this.$q.notify({
            type: "negative",
            message: "Failed to load images",
          });
          this.image_loading = false;
        });
      this.$q.notify({
        type: "positive",
        message: `${JSON.stringify(send_obj)}`,
      });
    },
    onRejected(rejectedEntries) {
      // Notify plugin needs to be installed
      // https://quasar.dev/quasar-plugins/notify#Installation
      console.log(rejectedEntries);
      this.$q.notify({
        type: "negative",
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`,
      });
    },
    onAdded(files) {
      // Obtain the uploaded file, you can change the logic if you are working with multiupload
      var file = files[0];

      // Create instance of FileReader
      var reader = new FileReader();

      // When the file has been succesfully read
      reader.onload = (event) => {
        // Create an instance of AudioContext
        var audioContext = new (window.AudioContext ||
          window.webkitAudioContext)();

        // Asynchronously decode audio file data contained in an ArrayBuffer.
        audioContext.decodeAudioData(event.target.result, (buffer) => {
          // Obtain the duration in seconds of the audio file (with milliseconds as well, a float value)
          this.duration = parseInt(buffer.duration);

          // example 12.3234 seconds
          console.log(
            "The duration of the song is of: " + this.duration + " seconds"
          );
          // Alternatively, just display the integer value with
          // parseInt(duration)
          // 12 seconds
        });
      };

      // In case that the file couldn't be read
      reader.onerror = function (event) {
        console.error("An error ocurred reading the file: ", event);
      };

      // Read file as an ArrayBuffer, important !
      reader.readAsArrayBuffer(file);

      this.output_images = [];
      this.duration = null;
      this.time_gap = null;
    },
  },
  computed: {
    num_intact: function () {
      if (
        this.duration === null ||
        this.time_gap === null ||
        this.time_gap <= 0
      )
        return 0;
      return parseInt(this.duration / this.time_gap);
    },
    num_non_intact: function () {
      if (
        this.duration === null ||
        this.time_gap === null ||
        this.time_gap <= 0
      )
        return 0;
      return this.duration % this.time_gap;
    },
  },
  data() {
    return {
      picture_options: [
        {
          label: "STFT 2D",
          value: "stft_2d",
        },
        {
          label: "STFT 3D",
          value: "stft_3d",
        },
        {
          label: "waveletes 2D",
          value: "waveletes_2d",
        },
        {
          label: "waveletes 3D",
          value: "waveletes_3d",
        },
      ],
      duration: null,
      time_gap: null,
      pictures: [],
      output_images: [],
      image_loading: false,
      viewer_options: {
        toolbar: false,
        inline: false,
        title: [1, (image, imageData) => `${image.alt}`],
        transition: false,
        rotatable: false,
        transition: false,
        navbar: false,
      },
    };
  },
};
</script>
