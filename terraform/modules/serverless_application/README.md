# application

End-to-end application infrastructure.

Hosts an application in ECS Fargate

---

## Useful commands

```
aws ecs describe-task-definition --task-definition template-application-test:4 > task_definition.json

aws ecs describe-services --cluster template-application-test --services template-application-test

aws codepipeline get-pipeline --name template-application-test > code_pipeline.json

aws codebuild batch-get-projects --names template-app-test > code_build.json
```