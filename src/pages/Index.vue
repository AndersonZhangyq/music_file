<template>
  <q-page>
    <div class="q-pa-md">
      <div class="row">
        Please choose your file type
      </div>
      <div class="row">
        <q-uploader
          url="http://localhost:4444/upload"
          label="WAV and MP3 file are accepted"
          accept=".wav, .mp3"
          @rejected="onRejected"
          @added="onAdded"
        />
      </div>
      <div class="row">
        Please choose the time gap which you want (in seconds):
      </div>
      <div class="row q-col-gutter-xs">
        <div class="col-1" v-for="(gap, index) in time_gap_options" :key="gap">
          <q-btn
            class="full-width"
            :label="gap"
            :color="index == gap_selected_idx ? 'red' : 'white'"
            :text-color="index == gap_selected_idx ? 'white' : 'black'"
            @click="gap_selected_idx = index"
          ></q-btn>
        </div>
      </div>
      <div class="row" v-if="gap_selected_idx != null">
        Please choose the segment which you want to visualize:
      </div>
      <div class="row q-col-gutter-xs" v-if="gap_selected_idx != null">
        <div
          class="col-1"
          v-for="(segment, index) in segment_options"
          :key="segment"
        >
          <q-btn
            class="full-width"
            :label="segment"
            :color="index == segment_selected_idx ? 'red' : 'white'"
            :text-color="index == segment_selected_idx ? 'white' : 'black'"
            @click="segment_selected_idx = index"
          ></q-btn>
        </div>
      </div>
      <div class="row">
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
    </div>
  </q-page>
</template>

<script>
export default {
  name: "PageIndex",
  methods: {
    submit: function() {
      if (this.gap_selected_idx == null) {
        this.$q.notify({
          type: "negative",
          message: "Please select the time gap"
        });
        return;
      }
      let gap_val = this.time_gap_options[this.gap_selected_idx];
      if (this.segment_selected_idx == null) {
        this.$q.notify({
          type: "negative",
          message: "Please select the segmentation"
        });
        return;
      }
      let seg_val = this.segment_options[this.segment_selected_idx];
      if (this.pictures.length == 0) {
        this.$q.notify({
          type: "negative",
          message: "Please select the picture"
        });
        return;
      }
      let send_obj = {
        gap_val: gap_val,
        seg_val: seg_val,
        pictures: this.pictures
      };
      console.log(send_obj);
    },
    onRejected(rejectedEntries) {
      // Notify plugin needs to be installed
      // https://quasar.dev/quasar-plugins/notify#Installation
      console.log(rejectedEntries);
      this.$q.notify({
        type: "negative",
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
      });
    },
    onAdded(files) {
      this.pictures = [];
      this.gap_selected_idx = null;
    }
  },
  watch: {
    gap_selected_idx(newVal) {
      this.segment_options = [];
      let start = 1;
      let gap_val = this.time_gap_options[newVal];
      while (start < 601) {
        let end = Math.min(600, start + gap_val - 1);
        this.segment_options.push(`${start} - ${end}`);
        start += gap_val;
      }
    }
  },
  data() {
    return {
      picture_options: [
        {
          label: "STFT 2D",
          value: "stft_2d"
        },
        {
          label: "STFT 3D",
          value: "stft_3d"
        },
        {
          label: "waveletes 2D",
          value: "waveletes_2d"
        },
        {
          label: "waveletes 3D",
          value: "waveletes_3d"
        }
      ],
      pictures: [],
      time_gap_options: [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        10,
        12,
        15,
        20,
        24,
        25,
        30,
        40,
        50,
        60,
        75,
        100,
        120,
        150,
        200,
        300,
        600
      ],
      gap_selected_idx: null,
      segment_options: [],
      segment_selected_idx: null
    };
  }
};
</script>
