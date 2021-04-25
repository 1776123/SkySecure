package com.qureshizaeem.skysecure;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {
    final FirebaseDatabase database = FirebaseDatabase.getInstance();
    Button b1, b2;
    TextView textView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        b1 = findViewById(R.id.b1);
        b2 = findViewById(R.id.b2);
        textView = findViewById(R.id.welcomemessage);
        b1.setBackgroundResource(R.drawable.buttonsstyle);
        b2.setBackgroundResource(R.drawable.buttonsstyle);
        database.getReference().child("coordinates") //originally log
                .addValueEventListener(new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot dataSnapshot) {
                        //finderobject is stuff from log in firebase
                        String z = dataSnapshot.child("coord0").getValue(String.class);
                        textView.setText("Weed Percentage: " + z);
                    }
                    @Override
                    public void onCancelled(DatabaseError databaseError) {
                    }
                });
    }

    public void clickB1(View view) {
        Intent intent = new Intent(this, MapActivity.class);
        startActivity(intent);
    }
}