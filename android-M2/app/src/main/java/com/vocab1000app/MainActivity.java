package com.vocab1000app;

import android.os.Bundle;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.community.tts.TextToSpeechPlugin;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(TextToSpeechPlugin.class);
        super.onCreate(savedInstanceState);
    }
}
