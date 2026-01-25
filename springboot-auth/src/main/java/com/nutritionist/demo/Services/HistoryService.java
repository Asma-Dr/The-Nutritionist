package com.nutritionist.demo.Services;

import org.springframework.stereotype.Service;
import com.nutritionist.demo.Iservices.IHistoryService;
import com.nutritionist.demo.Repositories.HistoryRepository;
import com.nutritionist.demo.Entities.History;
import com.nutritionist.demo.Entities.User;
import java.util.List;

@Service
public class HistoryService implements IHistoryService {
    private final HistoryRepository historyRepository;

    public HistoryService(HistoryRepository historyRepository) {
        this.historyRepository = historyRepository;
    }

    @Override
    public History saveHistory(History history) {
        return historyRepository.save(history);
    }

    @Override
    public List<History> getHistoryByUser(User user) {
        return historyRepository.findByUser(user);
    }
}
