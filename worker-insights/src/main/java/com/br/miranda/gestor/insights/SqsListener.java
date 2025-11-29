package com.br.miranda.gestor.insights;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.sqs.SqsClient;
import software.amazon.awssdk.services.sqs.model.DeleteMessageRequest;
import software.amazon.awssdk.services.sqs.model.Message;
import software.amazon.awssdk.services.sqs.model.ReceiveMessageRequest;

import java.net.URI;
import java.util.List;

@Service
public class SqsListener {


    @Value("${aws.sqs.endpoint.base}")
    private String sqsEndpointBase;

    @Value("${aws.sqs.queue.url}")
    private String queueUrl;


    public void receberMensagens() {

    }
}